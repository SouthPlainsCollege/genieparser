
# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device
from ats.topology import loader

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError

# iosxr show_evpn
from genie.libs.parser.iosxr.show_evpn import (ShowEvpnEvi,
                                               ShowEvpnEviDetail,
                                               ShowEvpnEthernetSegment,
                                               ShowEvpnEthernetSegmentDetail,
                                               ShowEvpnEthernetSegmentEsiDetail)


# ===================================================
#  Unit test for 'show evpn evi'
# ===================================================

class TestShowEvpnEvi(unittest.TestCase):

    '''Unit test for 'show evpn evi'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'evi': {
            1000: {
                'bridge_domain': 'VPWS:1000',
                'type': 'VPWS (vlan-unaware)',
            },
            2000: {
                'bridge_domain': 'XC-POD1-EVPN',
                'type': 'EVPN',
            },
            2001: {
                'bridge_domain': 'XC-POD2-EVPN',
                'type': 'EVPN',
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        RP/0/RSP1/CPU0:Router1#show evpn evi
        EVI        Bridge                       Domain Type
        ---------- ---------------------------- -------------------
        1000        VPWS:1000                   VPWS (vlan-unaware)
        2000        XC-POD1-EVPN                EVPN
        2001        XC-POD2-EVPN                EVPN

        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEvi(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEvi(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)

# ===================================================
#  Unit test for 'show evpn evi detail'
# ===================================================

class TestShowEvpnEviDetail(unittest.TestCase):

    '''Unit test for 'show evpn evi detail'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'evi': {
            145: {
                'bridge_domain': 'tb1-core1',
                'type': 'PBB',
                'unicast_label': '16000',
                'multicast_label': '16001',
                'rd_config': 'none',
                'rd_auto': '(auto) 1.100.100.100:145',
                'rt_auto': '100:145',
                'route_target_in_use': {
                    '100:145': {
                        'import': True,
                        'export': True,
                    },
                },
            },
            165: {
                'bridge_domain': 'tb1-core2',
                'type': 'PBB',
                'unicast_label': '16002',
                'multicast_label': '16003',
                'rd_config': 'none',
                'rd_auto': '(auto) 1.100.100.100:165',
                'rt_auto': '100:165',
                'route_target_in_use': {
                    '100:165': {
                        'import': True,
                        'export': True,
                    },
                },
            },
            185: {
                'bridge_domain': 'tb1-core3',
                'type': 'PBB',
                'unicast_label': '16004',
                'multicast_label': '16005',
                'rd_config': 'none',
                'rd_auto': '(auto) 1.100.100.100:185',
                'rt_auto': '100:185',
                'route_target_in_use': {
                    '100:185': {
                        'import': True,
                        'export': True,
                    },
                },
            },
            65535: {
                'bridge_domain': 'ES:GLOBAL',
                'type': 'BD',
                'unicast_label': '0',
                'multicast_label': '0',
                'rd_config': 'none',
                'rd_auto': '(auto) 1.100.100.100:0',
                'rt_auto': 'none',
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        RP/0/RSP0/CPU0:Router1#show evpn evi detail
        EVI        Bridge Domain                Type   
        ---------- ---------------------------- -------
        145        tb1-core1                    PBB 
        Unicast Label  : 16000
        Multicast Label: 16001
        RD Config: none
        RD Auto  : (auto) 1.100.100.100:145
        RT Auto  : 100:145
        Route Targets in Use           Type   
        ------------------------------ -------
        100:145                        Import 
        100:145                        Export 

        165        tb1-core2                    PBB 
        Unicast Label  : 16002
        Multicast Label: 16003
        RD Config: none
        RD Auto  : (auto) 1.100.100.100:165
        RT Auto  : 100:165
        Route Targets in Use           Type   
        ------------------------------ -------
        100:165                        Import 
        100:165                        Export 

        185        tb1-core3                    PBB 
        Unicast Label  : 16004
        Multicast Label: 16005
        RD Config: none
        RD Auto  : (auto) 1.100.100.100:185
        RT Auto  : 100:185
        Route Targets in Use           Type   
        ------------------------------ -------
        100:185                        Import 
        100:185                        Export 

        65535      ES:GLOBAL                    BD  
        Unicast Label  : 0
        Multicast Label: 0
        RD Config: none
        RD Auto  : (auto) 1.100.100.100:0
        RT Auto  : none
        Route Targets in Use           Type   
        ------------------------------ -------
        0100.9e00.0210                 Import 
        0100.be01.ce00                 Import 
        0100.be02.0101                 Import

        '''}
    
    golden_parsed_output2 = {
        'evi': {
            1: {
                'bridge_domain': 'core1',
                'type': 'PBB',
                'unicast_label': '24001',
                'multicast_label': '24002',
                'flow_label': 'N',
                'table-policy_name': 'forward_class_1',
                'forward-class': '1',
                'rd_config': 'none',
                'rd_auto': 'none',
                'rt_auto': 'none',
            },
        },
    }

    golden_output2 = {'execute.return_value': '''
        show evpn evi detail 
        Mon Aug 24 14:14:19.873 EDT

        EVI        Bridge Domain                Type   
        ---------- ---------------------------- -------
        1          core1                        PBB    
        Unicast Label  : 24001
        Multicast Label: 24002
        Flow Label: N
        Table-policy Name: forward_class_1
        Forward-class: 1
        RD Config: none
        RD Auto  : none
        RT Auto  : none
        Route Targets in Use           Type   
        ------------------------------ -------

        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEviDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEviDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)
    
    def test_golden2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output2)
        obj = ShowEvpnEviDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output2)

# ===================================================
#  Unit test for 'show evpn ethernet-segment'
# ===================================================

class test_show_evpn_ethernet_segment(unittest.TestCase):

    '''Unit test for 'show evpn ethernet-segment'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'segment_id': {
            '0012.1200.0000.0000.0000': {
                'interface': {
                    'Nv101': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0001.0000.0001': {
                'interface': {
                    'PW:40.40.40.40,10001': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0001.0000.0002': {
                'interface': {
                    'BE1': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0001.0000.0003': {
                'interface': {
                    'VFI:ves-vfi-1': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0002.0000.0001': {
                'interface': {
                    'PW:40.40.40.40,10011': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            '0012.1200.0002.0000.0003': {
                'interface': {
                    'VFI:ves-vfi-2': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
            'N/A': {
                'interface': {
                    'PW:40.40.40.40,10007': {
                        'next_hops': ['10.10.10.10'],
                    },
                    'PW:40.40.40.40,10017': {
                        'next_hops': ['10.10.10.10'],
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        show evpn ethernet-segment

        Ethernet Segment Id      Interface                          Nexthops
        ------------------------ ---------------------------------- --------------------
        0012.1200.0000.0000.0000 nv101                              10.10.10.10
        0012.1200.0001.0000.0001 PW:40.40.40.40,10001               10.10.10.10
        0012.1200.0001.0000.0002 BE1                                10.10.10.10
        0012.1200.0001.0000.0003 VFI:ves-vfi-1                      10.10.10.10
        0012.1200.0002.0000.0001 PW:40.40.40.40,10011               10.10.10.10
        0012.1200.0002.0000.0003 VFI:ves-vfi-2                      10.10.10.10
        N/A                      PW:40.40.40.40,10007               10.10.10.10
        N/A                      PW:40.40.40.40,10017               10.10.10.10
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEthernetSegment(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEthernetSegment(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)

# ===================================================
#  Unit test for 'show evpn ethernet-segment detail'
# ===================================================

class test_show_evpn_ethernet_segment_detail(unittest.TestCase):

    '''Unit test for 'show evpn ethernet-segment detail'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'segment_id': {
            '0210.0300.9e00.0210.0000': {
                'interface': {
                    'GigabitEthernet0/3/0/0': {
                        'next_hops': ['1.100.100.100', '2.100.100.100'],
                        'es_to_bgp_gates': 'Ready',
                        'es_to_l2fib_gates': 'Ready',
                        'main_port': {
                            'interface': 'GigabitEthernet0/3/0/0',
                            'if_handle': '0x1800300',
                            'state': 'Up',
                            'redundancy': 'Not Defined',
                        },
                        'source_mac': '0001.ed9e.0001 (PBB BSA)',
                        'topology': {
                            'operational': 'MHN',
                            'configured': 'A/A per service (default)',
                        },
                        'primary_services': 'Auto-selection',
                        'secondary_services': 'Auto-selection',
                        'service_carving_results': {
                            'bridge_ports': {
                                'num_of_total': 3,
                            },
                            'elected': {
                                'num_of_total': 0,
                            },
                            'not_elected': {
                                'num_of_total': 3,
                                'i_sid_ne': ['1450101', '1650205', '1850309'],
                            },
                        },
                        'mac_flushing_mode': 'STP-TCN',
                        'peering_timer': '45 sec [not running]',
                        'recovery_timer': '20 sec [not running]',
                        'flush_again_timer': '60 sec',
                    },
                },
            },
            'be01.0300.be01.ce00.0001': {
                'interface': {
                    'BE1': {
                        'next_hops': ['1.100.100.100', '2.100.100.100'],
                        'es_to_bgp_gates': 'Ready',
                        'es_to_l2fib_gates': 'Ready',
                        'main_port': {
                            'interface': 'Bundle-Ether1',
                            'if_handle': '0x000480',
                            'state': 'Up',
                            'redundancy': 'Active',
                        },
                        'source_mac': '0024.be01.ce00 (Local)',
                        'topology': {
                            'operational': 'MHN',
                            'configured': 'A/A per flow (default)',
                        },
                        'primary_services': 'Auto-selection',
                        'secondary_services': 'Auto-selection',
                        'service_carving_results': {
                            'bridge_ports': {
                                'num_of_total': 3,
                            },
                            'elected': {
                                'num_of_total': 3,
                                'i_sid_e': ['1450102', '1650206', '1850310'],
                            },
                            'not_elected': {
                                'num_of_total': 0,
                            },
                        },
                        'mac_flushing_mode': 'STP-TCN',
                        'peering_timer': '45 sec [not running]',
                        'recovery_timer': '20 sec [not running]',
                        'flush_again_timer': '60 sec',
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        Router#show evpn ethernet-segment detail
        Tue Jun 25 14:17:09.610 EDT
        Legend:
        A- PBB-EVPN load-balancing mode and Access Protection incompatible,
        B- no Bridge Ports PBB-EVPN enabled,
        C- Backbone Source MAC missing,
        E- ESI missing,
        H- Interface handle missing,
        I- Interface name missing,
        M- Interface in Down state,
        O- BGP End of Download missing,
        P- Interface already Access Protected,
        Pf-Interface forced single-homed,
        R- BGP RID not received,
        S- Interface in redundancy standby state,
        X- ESI-extracted MAC Conflict

        Ethernet Segment Id      Interface      Nexthops                                
        ------------------------ -------------- ----------------------------------------
        0210.0300.9e00.0210.0000 Gi0/3/0/0      1.100.100.100                           
                                                2.100.100.100                           
        ES to BGP Gates   : Ready
        ES to L2FIB Gates : Ready
        Main port         :
            Interface name : GigabitEthernet0/3/0/0
            IfHandle       : 0x1800300
            State          : Up
            Redundancy     : Not Defined
        Source MAC        : 0001.ed9e.0001 (PBB BSA)
        Topology          :
            Operational    : MHN
            Configured     : A/A per service (default)
        Primary Services  : Auto-selection
        Secondary Services: Auto-selection
        Service Carving Results:
            Bridge ports   : 3
            Elected        : 0
            Not Elected    : 3
                I-Sid NE  :  1450101, 1650205, 1850309
        MAC Flushing mode : STP-TCN
        Peering timer     : 45 sec [not running]
        Recovery timer    : 20 sec [not running]
        Flushagain timer  : 60 sec

        be01.0300.be01.ce00.0001 BE1            1.100.100.100                           
                                                2.100.100.100                           
        ES to BGP Gates   : Ready
        ES to L2FIB Gates : Ready
        Main port         :
            Interface name : Bundle-Ether1
            IfHandle       : 0x000480
            State          : Up
            Redundancy     : Active
        Source MAC        : 0024.be01.ce00 (Local)
        Topology          :
            Operational    : MHN
            Configured     : A/A per flow (default)
        Primary Services  : Auto-selection
        Secondary Services: Auto-selection
        Service Carving Results:
            Bridge ports   : 3
            Elected        : 3
                I-Sid E   :  1450102, 1650206, 1850310
            Not Elected    : 0
        MAC Flushing mode : STP-TCN
        Peering timer     : 45 sec [not running]
        Recovery timer    : 20 sec [not running]
        Flushagain timer  : 60 sec
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEthernetSegmentDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEthernetSegmentDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output1)

# ============================================================
#  Unit test for 'show evpn ethernet-segment esi {esi} detail'
# ============================================================

class TestShowEvpnEthernetSegmentEsiDetail(unittest.TestCase):

    '''Unit test for 'show evpn ethernet-segment esi {esi} detail'''
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'segment_id': {
            '0036.3700.0000.0000.1100': {
                'interface': {
                    'BE100': {
                        'next_hops': ['3.3.3.36', '3.3.3.37'],
                        'es_to_bgp_gates': 'Ready',
                        'es_to_l2fib_gates': 'Ready',
                        'main_port': {
                            'interface': 'Bundle-Ether100',
                            'interface_mac': '008a.9644.d8dd',
                            'if_handle': '0x0800001c',
                            'state': 'Up',
                            'redundancy': 'Not Defined',
                        },
                        'esi_type': 0,
                        'value': '36.3700.0000.0000.1100',
                        'es_import_rt': '3637.0000.0000 (from ESI)',
                        'source_mac': '0000.0000.0000 (N/A)',
                        'topology': {
                            'operational': 'MH, All-active',
                            'configured': 'All-active (AApF) (default)',
                        },
                        'service_carving': 'Auto-selection',
                        'peering_details': '3.3.3.36[MOD:P:00] 3.3.3.37[MOD:P:00]',
                        'service_carving_results': {
                            'forwarders': 1,
                            'permanent': 0,
                            'elected': {
                                'num_of_total': 1,
                            },
                            'not_elected': {
                                'num_of_total': 0,
                            },
                        },
                        'mac_flushing_mode': 'STP-TCN',
                        'peering_timer': '3 sec [not running]',
                        'recovery_timer': '30 sec [not running]',
                        'carving_timer': '0 sec [not running]',
                        'local_shg_label': 64005,
                        'remote_shg_label': 1,
                        'shg_label': {
                            64005: {
                                'next_hop': '3.3.3.37',
                            },
                            'num_of_label': 1,
                        },
                    },
                },
            },
        },
    }

    golden_output1 = {'execute.return_value': '''
        show evpn ethernet-segment esi 0036.3700.0000.0000.1100 detail

        Legend:

        B   - No Forwarders EVPN-enabled,

        C   - Backbone Source MAC missing (PBB-EVPN),

        RT  - ES-Import Route Target missing,

        E   - ESI missing,

        H   - Interface handle missing,

        I   - Name (Interface or Virtual Access) missing,

        M   - Interface in Down state,

        O   - BGP End of Download missing,

        P   - Interface already Access Protected,

        Pf  - Interface forced single-homed,

        R   - BGP RID not received,

        S   - Interface in redundancy standby state,

        X   - ESI-extracted MAC Conflict

        SHG - No local split-horizon-group label allocated

        

        Ethernet Segment Id      Interface                          Nexthops

        ------------------------ ---------------------------------- --------------------

        0036.3700.0000.0000.1100 BE100                              3.3.3.36

                                                                    3.3.3.37

        ES to BGP Gates   : Ready

        ES to L2FIB Gates : Ready

        Main port         :

            Interface name : Bundle-Ether100

            Interface MAC  : 008a.9644.d8dd

            IfHandle       : 0x0800001c

            State          : Up

            Redundancy     : Not Defined

        ESI type          : 0

            Value          : 36.3700.0000.0000.1100

        ES Import RT      : 3637.0000.0000 (from ESI)

        Source MAC        : 0000.0000.0000 (N/A)

        Topology          :

            Operational    : MH, All-active

            Configured     : All-active (AApF) (default)

        Service Carving   : Auto-selection

        Peering Details   : 3.3.3.36[MOD:P:00] 3.3.3.37[MOD:P:00]

        Service Carving Results:

            Forwarders     : 1

            Permanent      : 0

            Elected        : 1

            Not Elected    : 0

        MAC Flushing mode : STP-TCN

        Peering timer     : 3 sec [not running]

        Recovery timer    : 30 sec [not running]

        Carving timer     : 0 sec [not running]

        Local SHG label   : 64005

        Remote SHG labels : 1

                    64005 : nexthop 3.3.3.37
        '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowEvpnEthernetSegmentEsiDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(esi='0036.3700.0000.0000.1100')

    def test_golden1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowEvpnEthernetSegmentEsiDetail(device=self.device)
        parsed_output = obj.parse(esi='0036.3700.0000.0000.1100')
        self.assertEqual(parsed_output,self.golden_parsed_output1)

if __name__ == '__main__':
    unittest.main()