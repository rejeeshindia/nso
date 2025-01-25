# -*- mode: python; python-indent: 4 -*-
import ncs
import _ncs
from ncs.application import Service
from ncs.dp import Action


# ---------------
# ACTIONS EXAMPLE
# ---------------
class moveAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        _ncs.dp.action_set_timeout(uinfo,240)
        policy_list = [] 
        self.log.info('action name: ', name)
        self.log.info('Policy to Move: ', input.policy)
        self.log.info('After|Before|Top|Bottom: ', input.action)
        self.log.info('Positio: ', input.position)
        
        with ncs.maapi.single_write_trans('admin', 'admin') as trans:
            root = ncs.maagic.get_root(trans)
            if input.action == 'after':
                root.devices.device[input.device].config.fortinet_fmg__adom['TEST_ADOM'].policy_package['FGVM2VTM19001821-TEST'].firewall_policy.move(input.policy, ncs.maapi.MOVE_AFTER, input.position)
            elif input.action == 'before':
                root.devices.device[input.device].config.fortinet_fmg__adom['TEST_ADOM'].policy_package['FGVM2VTM19001821-TEST'].firewall_policy.move(input.policy, ncs.maapi.MOVE_BEFORE, input.position)
            elif input.action == 'top':
                root.devices.device[input.device].config.fortinet_fmg__adom['TEST_ADOM'].policy_package['FGVM2VTM19001821-TEST'].firewall_policy.move(input.policy, ncs.maapi.MOVE_FIRST)
            else:
                root.devices.device[input.device].config.fortinet_fmg__adom['TEST_ADOM'].policy_package['FGVM2VTM19001821-TEST'].firewall_policy.move(input.policy, ncs.maapi.MOVE_LAST)
            trans.apply()

class showAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        _ncs.dp.action_set_timeout(uinfo,240)
        self.log.info('action name: ', name)
        self.log.info('Show Device : ', input.device)


        policy_list = []         
        with ncs.maapi.single_read_trans('admin', 'admin') as trans:
            root = ncs.maagic.get_root(trans)
            for i in root.devices.device[input.device].config.fortinet_fmg__adom['TEST_ADOM'].policy_package['FGVM2VTM19001821-TEST'].firewall_policy:
                policy_list.append(i.policyid)
            self.log.info("Current Policies = ",str(policy_list))
            output.result = str(policy_list)




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
        self.register_action('pymove-action', moveAction)
        self.register_action('pyshow-action', showAction)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Action FINISHED')
