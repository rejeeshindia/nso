# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
from ncs.dp import Action


# ---------------
# ACTIONS EXAMPLE
# ---------------
class WrapperAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output):
        self.log.info('action name: ', name)
        self.log.info('user name: ', uinfo.username)

        user_device = []

        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, 'admin', 'admin'):
                with m.start_read_trans() as t:
                    root = ncs.maagic.get_root(t)

                    for group in root.nacm.groups.group:
                        for user_name in group.user_name:
                            if user_name == uinfo.username:
                                for device in group.device_name:
                                    user_device.append(device)

        if ((input.device1 in user_device) and (input.device2 in user_device)):
            try:
                with ncs.maapi.Maapi() as m:
                    with ncs.maapi.Session(m, 'admin', 'admin'):
                        with m.start_write_trans() as t:
                            root = ncs.maagic.get_root(t)

                            myservice = root.myservice.create(input.service_name)
                            myservice.device1 = input.device1
                            myservice.device2 = input.device2

                            t.apply()
                            output.result = 'Service is applied!'
            except Exception as e:
                ouput.result = e
        else:
            output.result = 'no access'


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Action(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Action RUNNING')

        # When using actions, this is how we register them:
        #
        self.register_action('myaction-action', WrapperAction)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Action FINISHED')
