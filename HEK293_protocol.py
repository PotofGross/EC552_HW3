from opentrons import protocol_api
from opentrons import labware

# metadata
metadata = {'apiLevel': '2.12',
    'protocolName': 'Plasmind to HEK293',
    'author': 'Drew Gross <agross13@bu.edu>',
    'description': 'Protocol to transfect plasmids into HEK293 cells'    
}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    # labware
    tryp_plate = protocol.load_labware('corning_24_wellplate_3.4ml_flat', 1)
    tiprack_big = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    tiprack_small = protocol.load_labware('opentrons_96_tiprack_20ul', 3)
    reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 4)

    temp_mod = protocol.load_module('temperature module gen2', 5)
    pcr_plate = protocol.load_labware('corning_24_wellplate_3.4ml_flat', 6)
    tuberack_15ml = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', 7)

    # pipette commands    # if using 24-well plate, only single channel pipette is loaded
    p300 = protocol.load_instrument('p300_single_gen2', mount='left', tip_racks=[tiprack_big, tiprack_small])
    p300.pick_up_tip(tiprack_big.wells()[0])
   
    pcr_plate.api_version('2.12')
    
    # reagent setup
    PBS = reservoir['A1']
    media = reservoir['A4']
    liquid_trash = reservoir['A9','A10']


    trypsin_volume = 250.0
    wash_volume = 100.0
    old_media_volume: 500.0
    new_media_volume= 500.0

    # add trypsin to old plate
    p300.starting_tip()
    p300.distribute(trypsin_volume, tuberack_15ml.wells()[0], tryp_plate.wells(), new_tip='once')

    p300.distribute(old_media_volume, media[0], tryp_plate.wells()[0], new_tip='once')

    ProtocolContext.delay(hours=24) #culture time

    # discard trypsin from old plate
    p300.consolidate(trypsin_volume + old_media_volume, tryp_plate.wells()[0], liquid_trash[0])
    # wash with PBS once
    p300.distribute(wash_volume, PBS.wells(), tryp_plate.wells()[0], new_tip='once')
    p300.consolidate(wash_volume, tryp_plate.wells()[0], liquid_trash[0])
    # add more media
    # mix with custom number of times
    p300.distribute(new_media_volume, media[0], tryp_plate.wells()[0], newtip='once')
    p300.mix(self, 3, p300.max_volume/2, tryp_plate.wells()[0], rate=1.0)
   

    # transfer half of the dissociated colony to a 24-well plate and rest of it
    # goes to an eppendorf tube
    p300.distribute(new_media_volume, media[0], pcr_plate.wells()[0], new_tip='once')
    p300.distribute(100,reservoir['A3'],pcr_plate.wells()[0],newtip='once') # dilutant

    temp_mod.set_temperature(37)
    p300.drop_tip()