from bottle import route, run, request, abort, static_file

from fsm import TocMachine


VERIFY_TOKEN = "123"
machine = TocMachine(
    states=[
        'init',
        'state_today',
        'state_hint',
        'state_detail',
        'state_tomorrow',
        'state_week',
        'state_month'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'state_today',
            'conditions': 'is_going_to_today'
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'state_tomorrow',
            'conditions': 'is_going_to_tomorrow'
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'state_week',
            'conditions': 'is_going_to_week'
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'state_month',
            'conditions': 'is_going_to_month'
        },
        {
            'trigger': 'advance',
            'source': 'state_today',
            'dest': 'state_hint',
            'conditions': 'is_going_to_hint'
        },
        {
            'trigger': 'advance',
            'source': 'state_today',
            'dest': 'state_detail',
            'conditions': 'is_going_to_detail'
        },
        {
            'trigger': 'advance',
            'source': 'state_hint',
            'dest': 'state_detail',
            'conditions': 'is_going_to_detail'
        },
        {
            'trigger': 'advance',
            'source': 'state_detail',
            'dest': 'state_hint',
            'conditions': 'is_going_to_hint'
        },
        {
            'trigger': 'advance',
            'source': [
                'state_today',
                'state_hint',
                'state_detail'
            ],
            'dest': 'init',
            'conditions': 'is_going_to_init'
        },
        {
            'trigger': 'go_back',
            'source': [
                'state_today',
                'state_hint',
                'state_detail',
                'state_tomorrow',
                'state_week',
                'state_month'
            ],
            'dest': 'init'
        }
    ],
    initial='init',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
