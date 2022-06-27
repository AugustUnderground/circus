""" Main Entry Point for Circus """

import sys
from flask import Flask, request, abort
from circus import rest

GPL_NOTICE = f"""
Circus Copyright (C) 2021 Electronics & Drives
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""

def handle_response(res):
    """
    HTTP Response Handler.
    """
    if isinstance(res, int):
        abort(res)
    elif res is None:
        abort(400)
    else:
        return res

def carnival():
    """
    Defines Flask Routes.
    """

    args   = rest.parser.parse_args()

    env_id, pdk, space, var, num, steps, host, port, scale, states, goals = \
            [ getattr(args, a) for a in
              [ 'env', 'pdk', 'space', 'var', 'num', 'step'
              , 'host', 'port', 'scale', 'states', 'goals' ] ]

    goals  = goals  or None
    states = states or 'perf'

    circ   = rest.make_env( env_id, pdk, space, var, num
                          , steps, scale, states, goals )

    route  = f'{env_id}-{pdk}-{space}-v{var}'

    app    = Flask('__main__')

    @app.route(f'/{route}/num_envs', methods=['GET'])
    def num_envs():
        res = {'num': num}
        return handle_response(res)

    @app.route(f'/{route}/reset', methods=['GET', 'POST'])
    def reset():
        req = request.json
        res = rest.reset( circ
                        , env_mask = req.get('env_mask', []) if req else []
                        , env_ids  = req.get('env_ids', [])  if req else []
                        , )
        return handle_response(res)

    @app.route(f'/{route}/restore', methods=['POST'])
    def restore():
        res = rest.restore(circ, request.json)
        return handle_response(res)

    @app.route(f'/{route}/restore_last', methods=['GET'])
    def restore_last():
        res = rest.restore_last(circ)
        return handle_response(res)

    @app.route(f'/{route}/step', methods=['POST'])
    def step():
        res = rest.step(circ, request.json)
        return handle_response(res)

    @app.route(f'/{route}/reward', methods=['POST'])
    def reward():
        res = rest.reward(circ, request.json)
        return handle_response(res)

    @app.route(f'/{route}/random_action', methods=['GET'])
    def random_action():
        res = rest.random_action(circ)
        return handle_response(res)

    @app.route(f'/{route}/random_step', methods=['GET'])
    def random_step():
        res = rest.random_step(circ)
        return handle_response(res)

    @app.route(f'/{route}/current_performance', methods=['GET'])
    def current_performance():
        res = rest.current_performance(circ)
        return handle_response(res)

    @app.route(f'/{route}/current_goal', methods=['GET'])
    def current_goal():
        res = rest.current_goal(circ)
        return handle_response(res)

    @app.route(f'/{route}/current_sizing', methods=['GET'])
    def current_sizing():
        res = rest.current_sizing(circ)
        return handle_response(res)

    @app.route(f'/{route}/last_action', methods=['GET'])
    def last_action():
        res = ( rest.current_sizing(circ)
                if space == 'geom' else
                rest.last_action(circ) )
        return handle_response(res)

    @app.route(f'/{route}/action_space', methods=['GET'])
    def action_space():
        res = rest.action_space(circ)
        return handle_response(res)

    @app.route(f'/{route}/action_keys', methods=['GET'])
    def action_keys():
        res = rest.action_keys(circ)
        return handle_response(res)

    @app.route(f'/{route}/observation_space', methods=['GET'])
    def observation_space():
        res = rest.observation_space(circ)
        return handle_response(res)

    @app.route(f'/{route}/observation_keys', methods=['GET'])
    def observation_keys():
        res = rest.observation_keys(circ)
        return handle_response(res)

    @app.route(f'/{route}/goal_keys', methods=['GET'])
    def goal_keys():
        res = rest.goal_keys(circ)
        return handle_response(res)

    @app.route(f'/{route}/num_steps', methods=['GET'])
    def goal_keys():
        res = rest.num_steps(circ)
        return handle_response(res)

    print('Launching Circus Server.')
    print(f'\tURL: http://{host}:{port}/{route}/')
    return app.run(host = host, port = port)

def main():
    """
    Do nothing, print GPL Notice.
    """
    print(GPL_NOTICE)
    return 0

if __name__ == '__main__':
    sys.exit(main())
