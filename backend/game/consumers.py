import json
from channels.generic.websocket import AsyncWebsocketConsumer
import random
import uuid

class GameConsumer(AsyncWebsocketConsumer):
    players_state = {}
    game_state = {}
    trial_state = {}
    round_state = {}
    ready_player = {}
    live_value = {}

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("game", self.channel_name)
        
        user_id = str(uuid.uuid4())[:6]
        user_class = 'player' if len([user for user in self.players_state.values() if user['class'] == 'player']) < 3 else 'admin'
        self.players_state[user_id] = {'class': user_class, 'ready': False, 'channel_name': self.channel_name}

        if user_class == 'player':
            self.ready_player[user_id] = False
            player_roles = [info.get("role") for info in self.game_state.values()]
            available_roles = ["Proposeur", "Commandeur", "Receveur"]

            for role in available_roles:
                if role not in player_roles:
                    new_role = role
                    break
            else:
                new_role = random.choice(available_roles)

            self.game_state[user_id] = {
                'id': user_id,
                'role': new_role,
                'reward': 0,
                'trial_played': 1,
                'round_played': 1
            }
        
            await self.send_state_update_to_players('players_state', self.players_state)
            await self.send(json.dumps({"type": "user_id", 'id': user_id }))
        else:
            await self.send_state_update('players_state', self.players_state)
            
    
    async def disconnect(self, code):
        user_id = self.get_user_id_by_channel_name(self.channel_name)
        if user_id is not None:
            user_class = self.players_state[user_id]['class']
            del self.players_state[user_id]

            if user_class == 'player':
                if user_id in self.game_state:
                    del self.game_state[user_id]
                    
                await self.send_state_update_to_players('players_state', self.players_state)
                await self.channel_layer.group_send("game", {
                    "type": "set_break_on",
                })

    def get_user_id_by_channel_name(self, channel_name):
        for user_id, user_info in self.players_state.items():
            if user_info['channel_name'] == channel_name:
                return user_id
        return None

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'setReady':
            await self.set_ready() # set players_state ready to true for the current player
        if data['type'] == 'update_trial_state':
            await self.update_trial_state(data['data']) # array from the front-end with role, proposition, commander_choice
        if data['type'] == 'update_round_state':
            await self.update_round_state()
        if data['type'] == 'get_game_state':
            await self.send_state_update_to_players('game_state', self.game_state)
        if data['type'] == 'get_trial_state':
            await self.send_state_update_to_players('trial_state', self.trial_state)
        if data['type'] == 'ready_round':
            await self.update_round_state(data['data'])
        if data['type'] == 'end_task':
            await self.end_task(data['data'])
        if data['type'] == 'player_state_ready':
            await self.player_ready(data['id'])
        if data['type'] == 'live_value_sent':
            await self.live_count_update(data['id'], data['value'])
        if data['type'] == 'post_max_value':
            await self.post_max_value(data['data'])

    async def player_ready(self, player_id):
        if player_id in self.ready_player:
            self.ready_player[player_id] = True

            ready_players = [p for p, ready in self.ready_player.items() if ready]
            if len(ready_players) == 3:
                await self.send_to_players(json.dumps({'type': 'all_player_state_ready'}))
                for user_id in self.ready_player.keys():
                    self.ready_player[user_id] = False

    async def set_ready(self):
        user_id = self.get_user_id_by_channel_name(self.channel_name)
        if user_id is not None:
            self.players_state[user_id]['ready'] = True
            await self.send_state_update_to_players('players_state', self.players_state)

            ready_players = [p for p in self.players_state.values() if p['class'] == 'player' and p['ready']]
            if len(ready_players) == 3:
                await self.send(json.dumps({'type': 'start_game'}))
                await self.reset_live_value_state()

    async def update_trial_state(self, data):
        print(data)
        self.trial_state.update(data)

        # if self.trial_state['id_trial'] > 1:
        #   self.trial_state = {'id_trial': 1, 'role_isPlaying': 'Proposeur', 'proposition': 0, 'commander_choice': None}

        await self.send_state_update_to_players('trial_state', self.trial_state)
    
    async def post_max_value(self, data):
        print(data)
        player_id = data['id']
        max_value = data['max']
        # Prepare the message to send to other players
        message = json.dumps({
            'type': 'player_max_value',
            'data': {'id': player_id, 'max': max_value},
        })

        # Send the message to the other players
        for other_id, other_info in self.players_state.items():
            if other_id != player_id and other_info['class'] == 'player':
                await self.channel_layer.send(
                    other_info['channel_name'],
                    {
                        "type": "send_message",
                        "message": message,
                    },
                )

    async def live_count_update(self, player_id, value):
        # Update the live_value state for the corresponding player_id
        self.live_value[player_id] = value

        # Send updated live_value state to other players, excluding their own ID
        for other_id, other_info in self.players_state.items():
            if other_id != player_id and other_info['class'] == 'player':
                # Create a list of other players' values, including the updated player
                other_players_values = [
                    {"id": other_player_id, "value": self.live_value.get(other_player_id, 0)}
                    for other_player_id in self.players_state
                    if other_player_id != other_id and self.players_state[other_player_id]['class'] == 'player'
                ]

                await self.channel_layer.send(
                    other_info['channel_name'],
                    {
                        "type": "send_message",
                        "message": json.dumps({'type': 'get_live_value', 'data': other_players_values}),
                    },
                )

    async def reset_live_value_state(self):
        self.live_value = {
            player_id: 0
            for player_id, player_info in self.players_state.items()
            if player_info['class'] == 'player'
        }

    async def update_round_state(self, data):
        print(data)
        user_id = data['id']
        self.round_state[user_id] = {'choice': data['choice'], 'role': data['role'], 'ready': data['ready']}

        if len(self.round_state) == 3 and all([player.get('ready', False) for player in self.round_state.values()]):
            await self.send_to_players(json.dumps({'type': 'start_round_choice'}))


    async def end_task(self, data):
        user_id = data['id']
        print(data)
        self.round_state[user_id].update({'value': data['value']})

        if all([player.get('value', None) is not None for player in self.round_state.values()]):
            await self.assign_role()

    async def assign_role(self):
        roles = ['Proposeur', 'Receveur', 'Commandeur']
        sorted_players = sorted(self.round_state.items(), key=lambda x: x[1]['value'], reverse=True)

        assigned_roles = []
        for i, (player_id, player_data) in enumerate(sorted_players):
            current_role = self.game_state[player_id]['role']
            if i == 0:
                if player_data['choice']:
                    remaining_roles = [r for r in roles if r != current_role]
                    new_role = random.choice(remaining_roles)
                else:
                    new_role = current_role
            else:
                if player_data['choice']:
                    remaining_roles = [r for r in roles if r != current_role and r not in assigned_roles]
                    if remaining_roles:
                        new_role = random.choice(remaining_roles)
                    else:
                        new_role = current_role
                else:
                    if current_role not in assigned_roles:
                        new_role = current_role
                    else:
                        remaining_roles = [r for r in roles if r not in assigned_roles]
                        new_role = random.choice(remaining_roles)

            assigned_roles.append(new_role)
            self.game_state[player_id]['role'] = new_role
            self.game_state[player_id]['round_played'] += 1

        await self.send_state_update_to_players('round_state', sorted_players)
        await self.send_state_update_to_players('game_state', self.game_state)
        await self.send(json.dumps({'type': 'assign_role_completed'}))

        for player_id in self.round_state.keys():
            self.round_state[player_id]['ready'] = False

        self.trial_state = {}
        await self.reset_live_value_state()

    # Helper functions for sending state updates to the frontend
    async def send_state_update_to_players(self, state_type, state_data):
        players_state_copy = dict(self.players_state)
        for user_id, user_info in players_state_copy.items():
            if user_info['class'] == 'player':
                await self.channel_layer.send(
                    user_info['channel_name'],
                    {
                        "type": "state_update",
                        "state_type": state_type,
                        "state_data": state_data,
                    },
                )

    async def send_state_update(self, state_type, state_data):
        message = {
            'type': state_type,
            'data': state_data
        }
        await self.send(json.dumps(message))

    async def broadcast_state_update(self, state_type, state_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'state_update',
                'state_type': state_type,
                'state_data': state_data,
            }
        )

    async def state_update(self, event):
        state_type = event['state_type']
        state_data = event['state_data']
        await self.send_state_update(state_type, state_data)

    async def set_break_on(self, event):
            await self.send(json.dumps({"type": "set_break_on"}))

    async def send_to_players(self, message):
        for user_id, user_info in self.players_state.items():
            if user_info['class'] == 'player':
                await self.channel_layer.send(
                    user_info['channel_name'],
                    {
                        "type": "send_message",
                        "message": message,
                    },
                )

    async def send_message(self, event):
        message = event['message']
        await self.send(message)
