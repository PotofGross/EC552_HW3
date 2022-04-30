from opentrons import protocol_api

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
    temp_mod = protocol.load_module('thermocyclerModuleV1')
    cell_plate = temp_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    pcr_plate = protocol.load_labware('corning_24_wellplate_3.4ml_flat', 6)
    tuberack_15ml = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', 5)

    # pipette commands    # if using 24-well plate, only single channel pipette is loaded
    p300 = protocol.load_instrument('p300_single_gen2', mount='left', tip_racks=[tiprack_big, tiprack_small])

    # reagent setup
    PBS = reservoir['A1']
    media = reservoir['A2']
    optiMEM = reservoir['A3']
    LipoLTX = reservoir['A4']

    liquid_trash = reservoir['A9']

    trypsin_volume = 250.0
    wash_volume = 100.0
    old_media_volume= 500.0
    new_media_volume= 500.0

    # add trypsin to old plate
    p300.distribute(trypsin_volume, tuberack_15ml.wells()[0], tryp_plate.wells(), new_tip='once')

    p300.distribute(old_media_volume, media, tryp_plate.wells()[0], new_tip='once')

    protocol.delay(minutes=24*60) #culture time

    # discard trypsin from old plate
    p300.consolidate(trypsin_volume + old_media_volume, tryp_plate.wells()[0], liquid_trash, new_tip='once')
    # wash with PBS once
    p300.distribute(wash_volume, PBS, tryp_plate.wells()[0], new_tip='once')
    p300.consolidate(wash_volume, tryp_plate.wells()[0], liquid_trash, new_tip='once')
    # add more media
    # mix with custom number of times
    p300.distribute(new_media_volume, media, tryp_plate.wells()[0], new_tip='once')
    p300.pick_up_tip()
    p300.mix(3, p300.max_volume/2, tryp_plate.wells()[0], rate=1.0)
    # transfer half of the dissociated colony to a 24-well plate and rest of it
    # goes to an eppendorf tube
    p300.drop_tip()
    p300.transfer(500,tryp_plate.wells()[0],pcr_plate.wells()[0], new_tip='once')
    p300.distribute(new_media_volume, media, pcr_plate.wells()[0], new_tip='once')
    p300.distribute(100,optiMEM,pcr_plate.wells()[0], newtip='once') # dilutant

    p300.distribute(250,LipoLTX,pcr_plate.wells()[0], new_tip='once') #reagent
    p300.pick_up_tip()
    p300.mix(3, p300.max_volume/2, pcr_plate.wells()[0], rate=1.0)
    p300.drop_tip()
    protocol.delay(minutes=30)

    p300.pick_up_tip()
    temp_mod.open_lid()
    for i in range(0,23):
        p300.transfer(100,pcr_plate.wells()[0],cell_plate.wells()[i],new_tip='never')
    p300.drop_tip()
    p300.pick_up_tip()
    p300.mix(3, p300.max_volume/2, cell_plate.wells()[0], rate=1.0)
    p300.drop_tip()
    temp_mod.set_block_temperature(37,hold_time_minutes=24*60, block_max_volume=100)
    temp_mod.close_lid()


    temp_mod.deactivate()