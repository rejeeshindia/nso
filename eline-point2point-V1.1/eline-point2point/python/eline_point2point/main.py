# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
from ncs.application import Application
import ncs.template
import sys

# --------------------------------------
# eline-point2point version 1.1 20180303
# --------------------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vars = ncs.template.Variables()

        # --- os & platform related code // a-side ---
        device = ''
        platform = ''
        model = ''
        os = ''
        loopback = ''
        device = service.__getitem__('a-side').__getitem__('device')

        m = ncs.maapi.Maapi()
        m.start_user_session('admin', 'system', [])

        t = m.start_trans(ncs.RUNNING, ncs.READ_WRITE)
        root = ncs.maagic.get_root(t)
        d=root.ncs__devices.device[device]

        model = d.platform.model
        os = d.platform.name
        if os == 'ios-xe':
            os = 'ios'
        if os == 'ios-xr':
            loopback = d.config.cisco_ios_xr__interface.Loopback.exists(1)
        if os == 'ios':
            loopback = d.config.ios__interface.Loopback.exists(1)

        t.finish()

        if model == 'ME-3600X-24FS-M':
            platform = 'ME-3600X'

        if model == 'ASR-920-24TZ-M':
            platform = 'ASR-920'

        if model == 'ASR9K':
            platform = 'ASR9K'

        if (model == 'NETSIM') and (os == 'ios'):
            platform = 'ME-3600X'

        if (model == 'NETSIM') and (os == 'ios-xr'):
            platform = 'ASR9K'

        if not loopback:
            sys.exit("The device a-side needs a Loopback1 interface")

        xgn = ''
        xgn = service.__getitem__('a-side').__getitem__('xconnect-group-name')

        if os == 'ios-xr':
            if xgn is None:
                sys.exit("For IOS-XR a-side devices an xconnect-group-name must be selected")

        vars.add('platform-a-side' , platform)
        vars.add('os-a-side' , os)

        # --- os & platform related code // z-side ---
        device = ''
        platform = ''
        model = ''
        os = ''
        loopback = ''
        device = service.__getitem__('z-side').__getitem__('device')

        m = ncs.maapi.Maapi()
        m.start_user_session('admin', 'system', [])
        t = m.start_trans(ncs.RUNNING, ncs.READ_WRITE)
        root = ncs.maagic.get_root(t)
        d=root.ncs__devices.device[device]

        model = d.platform.model
        os = d.platform.name
        if os == 'ios-xe':
            os = 'ios'
        if os == 'ios-xr':
            loopback = d.config.cisco_ios_xr__interface.Loopback.exists(1)
        if os == 'ios':
            loopback = d.config.ios__interface.Loopback.exists(1)

        t.finish()

        if model == 'ME-3600X-24FS-M':
            platform = 'ME-3600X'

        if model == 'ASR-920-24TZ-M':
            platform = 'ASR-920'

        if model == 'ASR9K':
            platform = 'ASR9K'

        if (model == 'NETSIM') and (os == 'ios'):
            platform = 'ME-3600X'

        if (model == 'NETSIM') and (os == 'ios-xr'):
            platform = 'ASR9K'

        if not loopback:
            sys.exit("The device z-side needs a Loopback1 interface")

        xgn = ''
        xgn = service.__getitem__('z-side').__getitem__('xconnect-group-name')

        if os == 'ios-xr':
            if xgn is None:
                sys.exit("For IOS-XR z-side devices an xconnect-group-name must be selected")

        vars.add('platform-z-side' , platform)
        vars.add('os-z-side' , os)

        # --- os & platform related code // z2-side ---
        device = ''
        platform = ''
        model = ''
        os = ''
        loopback = ''
        if service.__getitem__('backup-vc') == 'yes':
            device = service.__getitem__('z2-side').__getitem__('device')
            m = ncs.maapi.Maapi()
            m.start_user_session('admin', 'system', [])
            t = m.start_trans(ncs.RUNNING, ncs.READ_WRITE)
            root = ncs.maagic.get_root(t)
            d=root.ncs__devices.device[device]
            model = d.platform.model
            os = d.platform.name
            if os == 'ios-xe':
                os = 'ios'
            if os == 'ios-xr':
                loopback = d.config.cisco_ios_xr__interface.Loopback.exists(1)
            if os == 'ios':
                loopback = d.config.ios__interface.Loopback.exists(1)
            t.finish()
            if model == 'ME-3600X-24FS-M':
                platform = 'ME-3600X'
            if model == 'ASR-920-24TZ-M':
                platform = 'ASR-920'
            if model == 'ASR9K':
                platform = 'ASR9K'
            if (model == 'NETSIM') and (os == 'ios'):
                platform = 'ME-3600X'
            if (model == 'NETSIM') and (os == 'ios-xr'):
                platform = 'ASR9K'
            if not loopback:
                sys.exit("The device z2-side needs a Loopback1 interface")
            xgn = ''
            xgn = service.__getitem__('z2-side').__getitem__('xconnect-group-name')
            if os == 'ios-xr':
                if xgn is None:
                    sys.exit("For IOS-XR z2-side devices an xconnect-group-name must be selected")
        vars.add('platform-z2-side' , platform)
        vars.add('os-z2-side' , os)

        # --- interfaces // a-side ---
        ifnumber = ''
        interface = ''
        interfacetype = ''
        interfacenumber = ''

        ifnumber = service.__getitem__('a-side').__getitem__('GigabitEthernet')
        if ifnumber is not None:
            interface = 'GigabitEthernet' + ifnumber
            interfacetype = 'GigabitEthernet'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('a-side').__getitem__('TenGigE')
        if ifnumber is not None:
            interface = 'TenGigE' + ifnumber
            interfacetype = 'TenGigE'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('a-side').__getitem__('Bundle-Ether')
        if ifnumber is not None:
            interface = 'Bundle-Ether' + ifnumber
            interfacetype = 'Bundle-Ether'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('a-side').__getitem__('Ge')
        if ifnumber is not None:
            interface = 'GigabitEthernet' + ifnumber
            interfacetype = 'GigabitEthernet'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('a-side').__getitem__('Te')
        if ifnumber is not None:
            interface = 'TenGigabitEthernet' + ifnumber
            interfacetype = 'TenGigabitEthernet'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('a-side').__getitem__('Port-channel')
        if ifnumber is not None:
            interface = 'Port-channel' + ifnumber
            interfacetype = 'Port-channel'
            interfacenumber = ifnumber

        vars.add('interface-a-side' , interface)
        vars.add('interface-type-a-side' , interfacetype)
        vars.add('interface-number-a-side' , interfacenumber)

        # --- interfaces // z-side ---
        ifnumber = ''
        interface = ''
        interfacetype = ''
        interfacenumber = ''

        ifnumber = service.__getitem__('z-side').__getitem__('GigabitEthernet')
        if ifnumber is not None:
            interface = 'GigabitEthernet' + ifnumber
            interfacetype = 'GigabitEthernet'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('z-side').__getitem__('TenGigE')
        if ifnumber is not None:
            interface = 'TenGigE' + ifnumber
            interfacetype = 'TenGigE'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('z-side').__getitem__('Bundle-Ether')
        if ifnumber is not None:
            interface = 'Bundle-Ether' + ifnumber
            interfacetype = 'Bundle-Ether'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('z-side').__getitem__('Ge')
        if ifnumber is not None:
            interface = 'GigabitEthernet' + ifnumber
            interfacetype = 'GigabitEthernet'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('z-side').__getitem__('Te')
        if ifnumber is not None:
            interface = 'TenGigabitEthernet' + ifnumber
            interfacetype = 'TenGigabitEthernet'
            interfacenumber = ifnumber

        ifnumber = service.__getitem__('z-side').__getitem__('Port-channel')
        if ifnumber is not None:
            interface = 'Port-channel' + ifnumber
            interfacetype = 'Port-channel'
            interfacenumber = ifnumber

        vars.add('interface-z-side' , interface)
        vars.add('interface-type-z-side' , interfacetype)
        vars.add('interface-number-z-side' , interfacenumber)

        # --- interfaces // z2-side ---
        ifnumber = ''
        interface = ''
        interfacetype = ''
        interfacenumber = ''
        iamhere = ''

        if service.__getitem__('backup-vc') == 'yes':
            iamhere = service.__getitem__('z2-side').__getitem__('cpe')
            ifnumber = service.__getitem__('z2-side').__getitem__('GigabitEthernet')
            if ifnumber is not None:
                interface = 'GigabitEthernet' + ifnumber
                interfacetype = 'GigabitEthernet'
                interfacenumber = ifnumber
            ifnumber = service.__getitem__('z2-side').__getitem__('TenGigE')
            if ifnumber is not None:
                interface = 'TenGigE' + ifnumber
                interfacetype = 'TenGigE'
                interfacenumber = ifnumber
            ifnumber = service.__getitem__('z2-side').__getitem__('Bundle-Ether')
            if ifnumber is not None:
                interface = 'Bundle-Ether' + ifnumber
                interfacetype = 'Bundle-Ether'
                interfacenumber = ifnumber
            ifnumber = service.__getitem__('z2-side').__getitem__('Ge')
            if ifnumber is not None:
                interface = 'GigabitEthernet' + ifnumber
                interfacetype = 'GigabitEthernet'
                interfacenumber = ifnumber
            ifnumber = service.__getitem__('z2-side').__getitem__('Te')
            if ifnumber is not None:
                interface = 'TenGigabitEthernet' + ifnumber
                interfacetype = 'TenGigabitEthernet'
                interfacenumber = ifnumber
            ifnumber = service.__getitem__('z2-side').__getitem__('Port-channel')
            if ifnumber is not None:
                interface = 'Port-channel' + ifnumber
                interfacetype = 'Port-channel'
                interfacenumber = ifnumber
        vars.add('interface-z2-side' , interface)
        vars.add('interface-type-z2-side' , interfacetype)
        vars.add('interface-number-z2-side' , interfacenumber)
        vars.add('iamhere' , iamhere)

        # --- cpe models // a-side ---
        cpe = ''
        eoam = 'no'
        negauto = 'yes'
        l2tpacl = 'no'

        cpe = service.__getitem__('a-side').__getitem__('cpe')
        if cpe == 'uFalcon':
            eoam = 'yes'
            negauto = 'no'
            l2tpacl = 'no'

        if cpe == 'uFalcon SL':
            eoam = 'yes'
            negauto = 'yes'
            l2tpacl = 'no'

        if cpe == 'ME-3400':
            eoam = 'yes'
            negauto = 'no'
            l2tpacl = 'yes'

        if cpe == 'IE2000':
            eoam = 'no'
            negauto = 'yes'
            l2tpacl = 'no'

        vars.add('eoam-a-side' , eoam)
        vars.add('negauto-a-side' , negauto)
        vars.add('l2tpacl-a-side' , l2tpacl)

        # --- cpe models // z-side ---
        cpe = ''
        eoam = 'no'
        negauto = 'yes'
        l2tpacl = 'no'

        cpe = service.__getitem__('z-side').__getitem__('cpe')
        if cpe == 'uFalcon':
            eoam = 'yes'
            negauto = 'no'
            l2tpacl = 'no'

        if cpe == 'uFalcon SL':
            eoam = 'yes'
            negauto = 'yes'
            l2tpacl = 'no'

        if cpe == 'ME-3400':
            eoam = 'yes'
            negauto = 'no'
            l2tpacl = 'yes'

        if cpe == 'IE2000':
            eoam = 'no'
            negauto = 'yes'
            l2tpacl = 'no'

        vars.add('eoam-z-side' , eoam)
        vars.add('negauto-z-side' , negauto)
        vars.add('l2tpacl-z-side' , l2tpacl)

        # --- cpe models // z2-side ---
        cpe = ''
        eoam = 'no'
        negauto = 'yes'
        l2tpacl = 'no'

        if service.__getitem__('backup-vc') == 'yes':
            cpe = service.__getitem__('z2-side').__getitem__('cpe')
            if cpe == 'uFalcon':
                eoam = 'yes'
                negauto = 'no'
                l2tpacl = 'no'
            if cpe == 'uFalcon SL':
                eoam = 'yes'
                negauto = 'yes'
                l2tpacl = 'no'
            if cpe == 'ME-3400':
                eoam = 'yes'
                negauto = 'no'
                l2tpacl = 'yes'
            if cpe == 'IE2000':
                eoam = 'no'
                negauto = 'yes'
                l2tpacl = 'no'
        vars.add('eoam-z2-side' , eoam)
        vars.add('negauto-z2-side' , negauto)
        vars.add('l2tpacl-z2-side' , l2tpacl)

        # --- QoS related code // global ---
        bandwidth = service.__getitem__('product').__getitem__('product-bandwidth')
        burstbyte = bandwidth*1000000/8
        if burstbyte > 16000000:
            burstbyte = 16000000

        vars.add('product-cir-bps' , (bandwidth*1000000))
        vars.add('product-burst-byte' , burstbyte)
        vars.add('product-cir-kbps' , (bandwidth*1000))
        vars.add('product-burst-kbyte' , (bandwidth*1000/8))

        # --- VC related code // global ---
        vc = ''
        i = ''
        for i in service.__getitem__('name'):
            if i in '1234567890':
                vc+=i

        vars.add('vc-derived' , vc)

        vcbackup = ''
        vcbackup = '9' + vc
        vars.add('vc-backup-derived' , vcbackup)

        for var in vars:
            self.log.info(var)

        template = ncs.template.Template(service)
        template.apply('eline-point2point-template', vars)

    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('eline-point2point-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
