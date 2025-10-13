import configparser
from datetime import datetime

from dwarf_python_api.lib.dwarf_utils import perform_disconnect
from dwarf_python_api.lib.dwarf_utils import perform_goto
from dwarf_python_api.lib.dwarf_utils import perform_goto_stellar
from dwarf_python_api.lib.dwarf_utils import perform_time
from dwarf_python_api.lib.dwarf_utils import perform_timezone
from dwarf_python_api.lib.dwarf_utils import perform_calibration
from dwarf_python_api.lib.dwarf_utils import perform_stop_calibration
from dwarf_python_api.lib.dwarf_utils import perform_decoding_test
from dwarf_python_api.lib.dwarf_utils import perform_decode_wireshark
from dwarf_python_api.lib.dwarf_utils import read_longitude
from dwarf_python_api.lib.dwarf_utils import read_latitude
from dwarf_python_api.lib.dwarf_utils import read_camera_exposure
from dwarf_python_api.lib.dwarf_utils import read_camera_gain
from dwarf_python_api.lib.dwarf_utils import read_camera_IR
from dwarf_python_api.lib.dwarf_utils import read_camera_binning
from dwarf_python_api.lib.dwarf_utils import read_camera_format
from dwarf_python_api.lib.dwarf_utils import read_camera_count
from dwarf_python_api.lib.dwarf_utils import read_camera_wide_exposure
from dwarf_python_api.lib.dwarf_utils import read_camera_wide_gain
from dwarf_python_api.lib.dwarf_utils import parse_ra_to_float
from dwarf_python_api.lib.dwarf_utils import parse_dec_to_float
from dwarf_python_api.lib.dwarf_utils import perform_takeAstroPhoto
from dwarf_python_api.lib.dwarf_utils import perform_stopAstroPhoto
from dwarf_python_api.lib.dwarf_utils import perform_waitEndAstroPhoto
from dwarf_python_api.lib.dwarf_utils import perform_GoLive
from dwarf_python_api.lib.dwarf_utils import perform_takeWidePhoto
from dwarf_python_api.lib.dwarf_utils import perform_takeAstroWidePhoto
from dwarf_python_api.lib.dwarf_utils import perform_stopAstroWidePhoto
from dwarf_python_api.lib.dwarf_utils import perform_waitEndAstroWidePhoto
from dwarf_python_api.lib.dwarf_utils import perform_update_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_update_all_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_get_all_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_get_all_feature_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_get_all_camera_wide_setting
from dwarf_python_api.lib.dwarf_utils import unset_HostMaster
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_wifi_type
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_autoAP
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_country_list
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_country
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_psd
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_autoSTA
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_STA_ssid
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_STA_pwd
from dwarf_python_api.lib.dwarf_utils import motor_action
from dwarf_python_api.lib.dwarf_utils import perform_takePhoto
from dwarf_python_api.lib.dwarf_utils import perform_start_autofocus
from dwarf_python_api.lib.dwarf_utils import perform_stop_autofocus
from dwarf_python_api.lib.dwarf_utils import start_polar_align, stop_polar_align
from dwarf_python_api.lib.dwarf_utils import save_bluetooth_config_from_ini_file
from dwarf_python_api.lib.dwarf_utils import perform_get_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_reboot
from dwarf_python_api.lib.dwarf_utils import perform_powerdown

from dwarf_python_api.lib.data_utils import get_exposure_name_by_index
from dwarf_python_api.lib.data_utils import get_gain_name_by_index
from dwarf_python_api.lib.data_wide_utils import get_wide_exposure_name_by_index
from dwarf_python_api.lib.data_wide_utils import get_wide_gain_name_by_index

from dwarf_python_api.get_live_data_dwarf import get_live_data
import dwarf_python_api.get_config_data

from dwarf_ble_connect.connect_bluetooth import connect_bluetooth
from dwarf_ble_connect.lib.connect_direct_bluetooth import connect_ble_direct_dwarf, connect_ble_dwarf_win
from dwarf_python_api.lib.websockets_utils import get_client_status

# The config value for dwarf_id is offset by -1 (stored as one less than the actual ID).
# the value return by get_config_data must be used with these functions
from dwarf_python_api.get_config_data import config_to_dwarf_id_str, config_to_dwarf_id_int

def display_menu():
    print("")
    print("----------------------------------")
    print("  After the bluetooth connection, ")
    print("    a Time and Time Zone Frames   ")
    print("     are automatically sent.      ")
    print("----------------------------------")
    print("    Don't forget to send them     ")
    print("if not using bluetooth connection ")
    print("----------------------------------")
    print("1. Send Time Frame")
    print("2. Send TimeZone Frame")
    print("3. Send Calibration Frame")
    print("4. Send GoTo Polaris")
    print("5. Send GoTo Vega")
    print("6. Send GoTo M42")
    print("7. Send GoTo M31")
    print("8. Send GoTo Jupiter")
    print("9. Send GoTo Manual Target")
    print("10. Stop Calibration")
    print("11. Input Longitude & Latitude")
    print("12. Unset HOST MASTER")
    print("B. Bluetooth Functions")
    print("C. Camera Data Function")
    print("D. Force Disconnection")
    print("L. Get Live Data Function")
    print("M. Motor Function")
    print("P. Power Off The Dwarf")
    print("R. Reboot the Dwarf")
    print("S. Show Status data")
    print("T. Test Frames Decoding")
    print("0. Exit")

def display_menu_test():
    print("")
    print("------------------")
    print("T1. Decoding Test Frames 1")
    print("T2. Decoding Test Frames 2")
    print("T3. Decoding Test Frames 3")
    print("T4. Decoding All Test Frames")
    print("D. Decoding Unmasked Wireshark Frame")
    print("0. Return")

def display_menu_camera():
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = data_config['dwarf_id']
    print("")
    print("------------------")
    print("C1. Read Saved Config Camera Data")
    print("C2. Input Camera Data to Config")
    print("C3. Read Current Dwarf Camera Data")
    print("C4. Import Saved Config Camera Data into Dwarf")
    print("C5. Start Imaging Session")
    print("C6. Stop Imaging Session")
    print("C7. Wait until End of Imaging Session")
    print("C8. Go Live Action")
    print("C9. Take one Photo Only")
    print("C10. Astro Autofocus")
    print("C11. Astro Infinite Autofocus")
    print("C12. Stop Astro Autofocus")
    print("C13. Take one Wide Photo Only")

    if config_to_dwarf_id_str(dwarf_id) == "3":
        print("C14. Start Wide Imaging Session")
        print("C15. Stop Wide Imaging Session")
        print("C16. Wait until End of Wide Imaging Session")
    print("0. Return")

def display_menu_bluetooth():
    print("")
    print("------------------")
    print("C. connect Bluetooth and Start STA Mode with Browser")
    print("CD. connect Bluetooth and Start STA Mode with Python")
    print("CW. connect Bluetooth and Start STA Mode with Windows")
    print("R. Read Bluetooth Param Config Information")
    print("S. Save Bluetooth Param Config Information and for Connection")
    print("0. Return")

def display_menu_motor():
    print("")
    print("------------------")
    print("C. Closed Barrel Position")
    print("I. Init Horizontal Position")
    print("I3. Init Horizontal Position for D3")
    print("P. Polar Align Position")
    print("P3. Polar Align Position For D3")
    print("S. Turn 90° for Second Polar Align Position")
    print("S3. Turn 90° for Second Polar Align Position for D3")
    print("RR. Option RR. Reset Rotation Axis")
    print("RS. Option RS. Reset Pitch Axis")
    print("GP. Option GP. Read Position (D3 only)")
    print("PA. Option PA. Auto Polar align")
    print("PS. Option PS. Stop Polar align")
    print("0. Return")

def get_user_choice():
    try:
        choice = input("Enter your choice (1-12) or (B,C,D,L,M,P,R,S,T) or 0 to exit: ")
    except KeyboardInterrupt:
        print("Operation interrupted by the user (CTRL+C).")
        choice = '0'
    return choice

def get_user_choice_test():
    try:
        choice = input("Enter your choice (T1 to T4) or D or 0 to return to main menu: ")
    except KeyboardInterrupt:
        print("Operation interrupted by the user (CTRL+C).")
        choice = '0'
    return choice

def get_user_choice_camera():
    try:
        choice = input("Enter your choice (C1 to C16) or 0 to return to main menu: ")
    except KeyboardInterrupt:
        print("Operation interrupted by the user (CTRL+C).")
        choice = '0'
    return choice

def get_user_choice_bluetooth():
    try:
        choice = input("Enter your choice C,CD,CW,R,S or 0 to return to main menu: ")
    except KeyboardInterrupt:
        print("Operation interrupted by the user (CTRL+C).")
        choice = '0'
    return choice

def get_user_choice_motor():
    try:
        choice = input("Enter your choice C,I,P,P3,S or 0 to return to main menu: ")
    except KeyboardInterrupt:
        print("Operation interrupted by the user (CTRL+C).")
        choice = '0'
    return choice

def option_1():
    print("You selected Option 1: Send Time Frame")
    print("")
    # Add your Option 1 functionality here
    perform_time()

def option_2():
    print("You selected Option 2:  Send TimeZone Frame")
    print("")
    # Add your Option 2 functionality here
    perform_timezone()

def option_3():
    print("You selected Option 3: Send Calibration Frame")
    print("")
    # Add your Option 3 functionality here
    perform_calibration()

def option_4():
    print("You selected Option 4: Send GoTo Polaris")
    print("")
    # Add your Option 4 functionality here
    perform_goto_target("Polaris")

def option_5():
    print("You selected Option 5: Send GoTo Vega")
    print("")
    # Add your Option 5 functionality here
    perform_goto_target("Vega")

def option_6():
    print("You selected Option 6: Send GoTo M42")
    print("")
    # Add your Option 6 functionality here
    perform_goto_target("M42")

def option_7():
    print("You selected Option 7: Send GoTo M31")
    print("")
    # Add your Option 7 functionality here
    perform_goto_target("M31")

def option_8():
    print("You selected Option 8: Send GoTo Jupiter")
    print("")
    # Add your Option 8 functionality here
    select_solar_target("Jupiter")

def option_9():
    print("You selected Option 9: Manual Target")
    print("")
    # Add your Option 9 functionality here
    input_manual_target()

def option_10():
    print("You selected Option 11: Stop Calibration")
    perform_stop_calibration()
    # Add your Option 10 functionality here

def option_11():
    print("You selected Option 11: Input Data : Longitude, Latitude and TimeZone")
    input_data()
    # Add your Option 11 functionality here

def option_12():
    print("You selected Option 12: Set HOST MASTER")
    unset_HostMaster()
    # Add your Option 12 functionality here

def option_B():
    print("You selected Option B: Bluetooth Functions")
    choice_bluetooth()
    # Add your Option B functionality here

def option_C():
    print("You selected Option C: Camera Data function")
    choice_camera()
    # Add your Option C functionality here

def option_D():
    print("You selected Option D: Force Disconnection")
    perform_disconnect()
    # Add your Option D functionality here

def option_L():
    print("You selected Option L: Get Live Data Functions")
    get_live_data()
    # Add your Option L functionality here

def option_M():
    print("You selected Option M: Motor Functions")
    choice_motor()
    # Add your Option M functionality here

def option_P():
    print("You selected Option P: Power Off")
    perform_powerdown()
    # Add your Option P functionality here

def option_R():
    print("You selected Option R: Reboot")
    perform_reboot()
    # Add your Option R functionality here

def option_S():
    import json
    print("You selected Option S: Status Data")
    status = get_client_status()
    print(json.dumps(status, indent=4))
    # Add your Option M functionality here

def option_T():
    print("You selected Option T: Do Tests..")
    choice_test()
    # Add your Option T functionality here

def option_C1():
    print("You selected Option C1. Read Saved Config Camera Data")
    print("")
    # Add your Option C1 functionality here
    read_camera_data()

def option_C2():
    print("You selected Option C2. Input Camera Data to Config")
    print("")
    # Add your Option C2 functionality here
    input_camera_data()

def option_C3():
    print("You selected Option C3. Read Current Dwarf Camera Data")
    print("")
    # Add your Option C3 functionality here
    camera_exposure = False
    camera_gain = False
    camera_binning = False
    camera_IR = False
    camera_format = False
    camera_count = False
    camera_wide_exposure = False
    camera_wide_gain = False

    result = perform_get_all_camera_setting()
    result_feature = perform_get_all_feature_camera_setting()
    result_wide = perform_get_all_camera_wide_setting()
    print("------------------")

    # get dwarf type id
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = data_config['dwarf_id']
    print(f"Connected to Dwarf {config_to_dwarf_id_int(dwarf_id)}")

    # ALL PARAMS
    if (result and not isinstance(result,int)):
        # get Camera
        target_id = 0

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
           auto_mode = matching_entry["auto_mode"]
           print(f"The exposition mode is: {'Manual' if auto_mode else 'Auto'}")
           index_value = matching_entry["index"]

           camera_exposure = str(get_exposure_name_by_index(index_value,config_to_dwarf_id_str(dwarf_id)))
           print("the exposition is: ", camera_exposure)
        else:
           print("the exposition has not been found")

        # get Gain
        target_id = 1

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
           index_value = matching_entry["index"]


           camera_gain = str(get_gain_name_by_index(index_value,config_to_dwarf_id_str(dwarf_id)))
           print("the gain is: ", camera_gain)
        else:
           print("the gain has not been found")

        # get IR
        target_id = 8

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
            camera_IR = str(matching_entry["index"])

            if config_to_dwarf_id_str(dwarf_id) == "2":
                if (camera_IR == "0") :
                    print("the IR value is: IRCut")
                else:
                    print("the IR value is: IRPass")
            else :
                if (camera_IR == "0") :
                    print("the IR value is: VIS")
                elif (camera_IR == "1") :
                    print("the IR value is: ASTRO")
                else:
                    print("the IR value is: DUAL-BAND")
        else:
           print("the IRfilter has not been found")
    else:
       print("the exposition has not been found")
       print("the gain has not been found")
       print("the IRfilter has not been found")

    # ALL FEATURE PARAMS
    if (result_feature and not isinstance(result_feature,int)):
        # get binning
        target_id = 0

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_feature["all_feature_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
            camera_binning = str(matching_entry["index"])
            if (camera_binning == "0"):
                print("the Binning value is 4k")
            else:
                print("the Binning value is 2k")
        else:
           print("the Binning value has not been found")

        # get camera_format
        target_id = 2

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_feature["all_feature_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
            camera_format = str(matching_entry["index"])
            if (camera_format == "0"):
                print("the image format value is: FITS")
            else:
                print("the image format value is: TIFF")
        else:
           print("the image format value has not been found")

        # get camera_count
        target_id = 1

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_feature["all_feature_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
            camera_count = str(round(matching_entry["continue_value"]))

            print("the number of images for the session is:", camera_count)
        else:
           print("the number of images for the session has not been found")
    else:
       print("the Binning value has not been found")
       print("the image format value has not been found")
       print("the number of images for the session has not been found")

    # ALL Wide PARAMS
    if (result_wide and not isinstance(result_wide,int)):
        # get Camera
        target_id = 0

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_wide["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
           auto_mode = matching_entry["auto_mode"]
           print(f"The wide exposition mode is: {'Manual' if auto_mode else 'Auto'}")
           index_value = matching_entry["index"]

           camera_wide_exposure = str(get_wide_exposure_name_by_index(index_value,config_to_dwarf_id_str(dwarf_id)))
           print("the wide exposition is: ", camera_wide_exposure)
        else:
           print("the wide exposition has not been found")

        # get Gain
        target_id = 1

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_wide["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
           index_value = matching_entry["index"]

           camera_wide_gain = str(get_wide_gain_name_by_index(index_value,config_to_dwarf_id_str(dwarf_id)))
           print("the wide gain is: ", camera_wide_gain)
        else:
           print("the wide gain has not been found")

    # error no response on D3
    # print("direct=> the wide gain is: ", perform_get_camera_setting("wide_gain"))
    

def option_C4():
    print("You selected Option C4. Import Saved Config Camera Data into Dwarf")
    print("")
    # Add your Option C4 functionality here
    # get dwarf type id
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = data_config['dwarf_id']
    print(f"Connected to Dwarf {config_to_dwarf_id_int(dwarf_id)}")

    if (camera_exposure := read_camera_exposure()):
        print("the exposition is: ", camera_exposure)
        perform_update_camera_setting("exposure", camera_exposure, config_to_dwarf_id_str(dwarf_id))

    if (camera_gain := read_camera_gain()):
        print("the gain is:", camera_gain)
        perform_update_camera_setting("gain", camera_gain, config_to_dwarf_id_str(dwarf_id))

    if (camera_IR := read_camera_IR()):
        print("the IR value is:", camera_IR)
        perform_update_camera_setting("IR", camera_IR)

    if (camera_binning := read_camera_binning()):
        print("the Binning value is:", camera_binning)
        perform_update_camera_setting("binning", camera_binning)

    if (camera_format := read_camera_format()):
        print("the image format value is:", camera_format)
        perform_update_camera_setting("fileFormat", camera_format)

    if (camera_count := read_camera_count()):
        print("the number of images for the session is:", camera_count)
        perform_update_camera_setting("count", camera_count)

    if (camera_wide_exposure := read_camera_wide_exposure()):
        print("the wide exposition is: ", camera_wide_exposure)
        perform_update_camera_setting("wide_exposure", camera_wide_exposure, config_to_dwarf_id_str(dwarf_id))

    if (camera_wide_gain := read_camera_wide_gain()):
        print("the wide gain is:", camera_wide_gain)
        perform_update_camera_setting("wide_gain", camera_wide_gain, config_to_dwarf_id_str(dwarf_id))

def option_CT4():
    print("You selected Option CT4. Import Saved Config All Tele Camera all Data into Dwarf")
    print("")
    # Add your Option CW4 functionality here
    # get dwarf type id
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = data_config['dwarf_id']
    dwarf_id_int = config_to_dwarf_id_int(dwarf_id)
    print(f"Connected to Dwarf {'Mini' if dwarf_id_int == 5 else dwarf_id_int}")

    allValue = {
        'camera_exposure': False,
        'camera_gain': False,
        'camera_ircut': 0,
        'camera_wb_mode': 0,
        'camera_wb_index_type': 2,
        'camera_wb_index': 0,
        'camera_brightness': 0,
        'camera_contrast': 0,
        'camera_saturation': 0,
        'camera_sharpness': 50,
        'camera_jpg_quality': 80
    }
    allValue['camera_exposure'] = read_camera_exposure()
    if (allValue['camera_exposure']):
        print("the wide exposition is: ", allValue['camera_exposure'])

    allValue['camera_gain'] = read_camera_gain()
    if (allValue['camera_gain']):
        print("the wide gain is:", allValue['camera_gain'])

    perform_update_all_camera_setting("tele", allValue, config_to_dwarf_id_str(dwarf_id))

def option_CW4():
    print("You selected Option CW4. Import Saved Config All Wide Camera all Data into Dwarf")
    print("")
    # Add your Option CW4 functionality here
    # get dwarf type id
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = data_config['dwarf_id']
    dwarf_id_int = config_to_dwarf_id_int(dwarf_id)
    print(f"Connected to Dwarf {'Mini' if dwarf_id_int == 5 else dwarf_id_int}")

    allValue = {
        'camera_exposure': False,
        'camera_gain': False,
        'camera_ircut': 0,
        'camera_wb_mode': 0,
        'camera_wb_index_type': 2,
        'camera_wb_index': 0,
        'camera_brightness': 0,
        'camera_contrast': 0,
        'camera_saturation': 0,
        'camera_sharpness': 50,
        'camera_jpg_quality': 80
    }
    allValue['camera_exposure'] = read_camera_wide_exposure()
    if (allValue['camera_exposure']):
        print("the wide exposition is: ", allValue['camera_exposure'])

    allValue['camera_gain'] = read_camera_wide_gain()
    if (allValue['camera_gain']):
        print("the wide gain is:", allValue['camera_gain'])

    perform_update_all_camera_setting("wide", allValue, config_to_dwarf_id_str(dwarf_id))
def option_C5():
    print("You selected Option C5. Start Imaging Session")
    print("")
    # Add your Option C5 functionality here
    perform_takeAstroPhoto()

def option_C6():
    print("You selected Option C6. Stop Imaging Session")
    print("")
    # Add your Option C6 functionality here
    perform_stopAstroPhoto()

def option_C7():
    print("You selected Option C7. Wait until End of Imaging Session")
    print("")
    # Add your Option C7 functionality here
    perform_waitEndAstroPhoto()

def option_C8():
    print("You selected Option C8. Go Live Action")
    print("")
    # Add your Option C8 functionality here
    perform_GoLive()

def option_C9():
    print("You selected Option C9. Take one Photo Only")
    print("")
    # Add your Option C9 functionality here
    perform_takePhoto()

def option_C10():
    print("You selected Option C10. Astro Autofocus")
    print("")
    # Add your Option C10 functionality here
    perform_start_autofocus(False)

def option_C11():
    print("You selected Option C11. Astro Infinite Autofocus")
    print("")
    # Add your Option C11 functionality here
    perform_start_autofocus(True)

def option_C12():
    print("You selected Option C12. Stop Astro Autofocus")
    print("")
    # Add your Option C12 functionality here
    perform_stop_autofocus()

def option_C13():
    print("You selected Option C13, Take one Wide Photo Only")
    print("")
    # Add your Option C13 functionality here
    perform_takeWidePhoto()

def option_C14():
    print("You selected Option C13, Start Wide Imaging Session")
    print("")
    # Add your Option C14 functionality here
    perform_takeAstroWidePhoto()

def option_C15():
    print("You selected Option C15, Stop Wide Imaging Session")
    print("")
    # Add your Option C15 functionality here
    perform_stopAstroWidePhoto()

def option_C16():
    print("You selected Option C16. Wait until End of Wide Imaging Session")
    print("")
    # Add your Option C16 functionality here
    perform_waitEndAstroWidePhoto()

def option_BC():
    print("You selected Option C. connect Bluetooth and Start STA Mode")
    print("")
    # Add your Option BC functionality here
    if (connect_bluetooth()):
        
        #init Frame : TIME and TIMZONE
        result = perform_time()
       
        if result:
           perform_timezone()

def option_BCD():
    print("You selected Option CD. connect Bluetooth and Start STA Mode with Python")
    print("")
    # Add your Option BCD functionality here
    ble_psd = read_bluetooth_ble_psd() or "DWARF_12345678" 
    ble_STA_ssid = read_bluetooth_ble_STA_ssid() or ""
    ble_STA_pwd = read_bluetooth_ble_STA_pwd() or ""
    # Test Auto Select
    auto_select = "" # "DWARF3_3AD246" or 0 to give the list and "" to connect to the first after 10 s

    if (connect_ble_direct_dwarf(ble_psd, ble_STA_ssid, ble_STA_pwd,auto_select)):
        
        #init Frame : TIME and TIMZONE
        result = perform_time()
       
        if result:
           perform_timezone()

def option_BCW():
    print("You selected Option CW. connect Bluetooth and Start STA Mode with Windows")
    print("")
    # Add your Option BCW functionality here
    ble_psd = read_bluetooth_ble_psd() or "DWARF_12345678" 
    ble_STA_ssid = read_bluetooth_ble_STA_ssid() or ""
    ble_STA_pwd = read_bluetooth_ble_STA_pwd() or ""

    if (connect_ble_dwarf_win(ble_psd, ble_STA_ssid, ble_STA_pwd)):
        
        #init Frame : TIME and TIMZONE
        result = perform_time()
       
        if result:
           perform_timezone()

def option_BR():
    print("You selected Option R. Read Bluetooth Param Config Information")
    print("")
    # Add your Option BR functionality here
    read_bluetooth_data()

def option_BS():
    print("You selected Option S. Save Bluetooth Param Config Information")
    print("")
    # Add your Option BS functionality here
    input_bluetooth_data()

def option_MC():
    print("You selected Option C. Closed Barrel Position")
    print("")
    # Add your Option MC functionality here
    motor_action(1)

def option_MI():
    print("You selected Option I. Init Horizontal Position")
    print("")
    # Add your Option MI functionality here
    motor_action(2)

def option_MI3():
    print("You selected Option I. Init Horizontal Position for D3")
    print("")
    # Add your Option MI functionality here
    motor_action(9)

def option_MP():
    print("You selected Option P. Polar Align Position")
    print("")
    # Add your Option MP functionality here
    motor_action(3)

def option_MP3():
    print("You selected Option P. Polar Align Position for D3")
    print("")
    # Add your Option MP functionality here
    motor_action(7)

def option_MS():
    print("You selected Option S. Turn 90° for Second Polar Align Position")
    print("")
    # Add your Option MS functionality here
    motor_action(4)

def option_MS3():
    print("You selected Option S. Turn 90° for Second Polar Align Position for D3")
    print("")
    # Add your Option MS functionality here
    motor_action(4,0.5)

def option_RR():
    print("You selected Option RR. Reset Rotation Axis")
    print("")
    # Add your Option RR functionality here
    motor_action(5)

def option_RS():
    print("You selected Option RS.  Reset Pitch Axis")
    print("")
    # Add your Option RS functionality here
    motor_action(6)

def option_GP():
    print("You selected Option GP.  Read Position")
    print("")
    # Add your Option GP functionality here
    motor_action(8)

def option_PA():
    print("You selected Option PA.  Auto Polar align")
    print("")
    # Add your Option GP functionality here
    start_polar_align()

def option_PS():
    print("You selected Option PS.  Stop Polar align")
    print("")
    # Add your Option GP functionality here
    stop_polar_align()

def option_20():
    print("You selected Option T1: Decoding Test Frames 1")
    print("")
    # Add your Option T1 functionality here
    perform_decoding_test(True, False, False)

def option_21():
    print("You selected Option T2: Decoding Test Frames 2")
    print("")
    # Add your Option T2 functionality here
    perform_decoding_test(False, True, False)

def option_22():
    print("You selected Option T3: Decoding Test Frames 3")
    print("")
    # Add your Option T3 functionality here
    perform_decoding_test(False, False, True)

def option_23():
    print("You selected Option T4: Decoding Test All Frames")
    print("")
    # Add your Option T4 functionality here
    perform_decoding_test(True, True, True)

def option_24():
    print("You selected Option D. Decoding Unmasked Wireshark Frame")
    print("")
    # Add your Option D1 functionality here
    return input_frame(False)

def input_data():
    user_longitude = input("Enter your Longitude: ")
    print("You entered:", user_longitude)
    user_latitude = input("Enter your Latitude: ")
    print("You entered:", user_latitude)
    user_timezone = input("Enter your TimeZone: ")
    print("You entered:", user_timezone)
    print("")
    update_config(user_longitude, user_latitude, user_timezone)

def validate_input(input_str, min, max):
    try:
        if '/' in input_str:
            # Handle fraction input
            numerator, denominator = input_str.split("/")

            # Convert to integers
            numerator = int(numerator)
            denominator = int(denominator)

            # Check for zero division
            if denominator == 0:
                print("Invalid input. Denominator cannot be zero.")
                return False

            # Perform the division to get the decimal value
            result = numerator / denominator

        else:
            # Handle decimal or integer input
            result = float(input_str)  # Automatically handles both decimal and integer inputs

        # Check if result is greater than 0 and less than 100
        if min < result < max:
            return True
        else:
            print(f"Invalid input. The value is not between {min} and {max}.")
            return False
    
    except ValueError:
        print("Invalid input. Please provide a valid integer or fraction.")
        return False

def input_camera_data():
    # get dwarf type id
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = data_config['dwarf_id']
    print(f"connected to Dwarf {config_to_dwarf_id_int(dwarf_id)}")
    if config_to_dwarf_id_str(dwarf_id) == "2":
        prompt = "Enter the desired exposition in seconds (0 = auto - 60), use fraction for less than 1s (ex: 1/10):"
    else:
        prompt = "Enter the desired exposition in seconds (0 = auto - 15), use fraction for less than 1s (ex: 1/10):"
    camera_exposure_init = read_camera_exposure()
    camera_exposure = input(f"{prompt}[{camera_exposure_init}]:") if camera_exposure_init else input(prompt+"[1]")
    if not camera_exposure and not camera_exposure_init:
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif config_to_dwarf_id_str(dwarf_id) == "1" and camera_exposure and not validate_input(camera_exposure, 0, 15):
        print("Input Data Error:", camera_exposure)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif config_to_dwarf_id_str(dwarf_id) == "3" and camera_exposure and not validate_input(camera_exposure, 0, 60):
        print("Input Data Error:", camera_exposure)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif (camera_exposure):
        print("You entered:", camera_exposure)
    elif config_to_dwarf_id_str(dwarf_id) == "2" and camera_exposure_init and not validate_input(camera_exposure_init, 0, 15):
        print("Input Data Error:", camera_exposure_init)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif config_to_dwarf_id_str(dwarf_id) == "3" and camera_exposure_init and not validate_input(camera_exposure_init, 0, 60):
        print("Input Data Error:", camera_exposure_init)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif (camera_exposure_init):
        camera_exposure = camera_exposure_init
        print("Saved value used:", camera_exposure)
    else:
        print("No value entered:")

    camera_gain_init = read_camera_gain()
    prompt = "Enter the desired gain between (0-240):"
    camera_gain = input(f"{prompt}[{camera_gain_init}]:") if camera_gain_init else input(prompt+"[80]")
    if not camera_gain and not camera_gain_init:
        camera_gain = "80"
        print("Set to Default:", camera_gain)
    elif camera_gain and (int(camera_gain)<0 or int(camera_gain) > 240):
        print("Input Data Error:", camera_gain)
        camera_gain = "80"
        print("Set to Default:", camera_gain)
    elif (camera_gain):
        print("You entered:", camera_gain)
    elif (camera_gain_init):
        camera_gain = camera_gain_init
        print("Saved value used:", camera_gain)
    else:
        print("No value entered:")

    camera_IR_init = read_camera_IR()
    if config_to_dwarf_id_str(dwarf_id) == "2":
        prompt = "Enter the desired IR value: 0 for IRCut, 1 for IRPass:"
    else:
        prompt = "Enter the desired IR value: 0 for VIS, 1 for ASTRO, 2 for DUAL-BAND:"
    camera_IR = input(f"{prompt}[{camera_IR_init}]:") if camera_IR_init else input(prompt+"[IRCut]")
    if not camera_IR and not camera_IR_init:
        camera_IR = "0"
        if config_to_dwarf_id_str(dwarf_id) == "2":
            print("Set to Default (IRCut):", camera_IR)
        else:
            print("Set to Default (VIS):", camera_IR)
    elif camera_IR and (camera_IR!="0" and camera_IR !="1" and config_to_dwarf_id_str(dwarf_id) == "2"):
        print("Input Data Error:", camera_IR)
        camera_IR = "0"
        print("Set to Default (IRCut):", camera_IR)
    elif camera_IR and (camera_IR!="0" and camera_IR !="1" and camera_IR !="2" and config_to_dwarf_id_str(dwarf_id) == "3"):
        print("Input Data Error:", camera_IR)
        camera_IR = "0"
        print("Set to Default (VIS):", camera_IR)
    else:
        print("You entered:", camera_IR)

    camera_binning_init = read_camera_binning()
    prompt = "Enter the desired Binning value: 0 for 4k, 1 for 2k:"
    camera_binning = input(f"{prompt}[{camera_binning_init}]:") if camera_binning_init else input(prompt+"[4k]")
    if not camera_binning and not camera_binning_init:
        camera_binning = "0"
        print("Set to Default (4k):", camera_binning)
    elif camera_binning and (camera_binning!="0" and camera_binning !="1"):
        print("Input Data Error:", camera_binning)
        camera_binning = "0"
        print("Set to Default (4k):", camera_binning)
    else:
        print("You entered:", camera_binning)

    camera_format_init = read_camera_format()
    prompt = "Enter the desired image format value: 0 for FITS, 1 for TIFF:"
    camera_format = input(f"{prompt}[{camera_format_init}]:") if camera_format_init else input(prompt+"[FITS]")
    if not camera_format and not camera_format_init:
        camera_format = "0"
        print("Set to Default (FITS):", camera_format)
    elif camera_format and (camera_format!="0" and camera_format !="1"):
        print("Input Data Error:", camera_format)
        camera_format = "0"
        print("Set to Default (FITS):", camera_format)
    else:
        print("You entered:", camera_format)

    camera_count_init = read_camera_count()
    prompt = "Enter the desired number of images for the session between (1-999)"
    camera_count = input(f"{prompt}[{camera_count_init}]:") if camera_count_init else input(prompt+"[999]")
    if not camera_count and not camera_count_init:
        camera_count = "999"
        print("Set to Default:", camera_count)
    elif camera_count and (int(camera_count)<1 or int(camera_count) > 999):
        print("Input Data Error:", camera_count)
        camera_count = "999"
        print("Set to Default:", camera_count)
    else:
        print("You entered:", camera_count)

    if config_to_dwarf_id_str(dwarf_id) == "3":
        prompt = "Enter the desired wide exposition in seconds (0 = auto - 60), use fraction for less than 1s (ex: 1/10):"
    else:
        prompt = "Enter the desired wide exposition in seconds (0 = auto - 1.0), use fraction for less than 1s (ex: 1/10):"
    camera_wide_exposure_init = read_camera_wide_exposure()
    camera_wide_exposure = input(f"{prompt}[{camera_wide_exposure_init}]:") if camera_wide_exposure_init else input(prompt+"[1]")
    if not camera_wide_exposure and not camera_wide_exposure_init:
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif config_to_dwarf_id_str(dwarf_id) == "2" and camera_wide_exposure and not validate_input(camera_wide_exposure, 0, 15):
        print("Input Data Error:", camera_wide_exposure)
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif config_to_dwarf_id_str(dwarf_id) == "3" and camera_wide_exposure and not validate_input(camera_wide_exposure, 0, 60):
        print("Input Data Error:", camera_wide_exposure)
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif (camera_wide_exposure):
        print("You entered:", camera_wide_exposure)
    elif config_to_dwarf_id_str(dwarf_id) == "2" and camera_wide_exposure_init and not validate_input(camera_wide_exposure_init, 0, 15):
        print("Input Data Error:", camera_wide_exposure)
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif config_to_dwarf_id_str(dwarf_id) == "3" and camera_wide_exposure_init and not validate_input(camera_wide_exposure_init, 0, 60):
        print("Input Data Error:", camera_wide_exposure_init)
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif (camera_wide_exposure_init):
        camera_wide_exposure = camera_wide_exposure_init
        print("Saved value used:", camera_wide_exposure)
    else:
        print("No value entered:")

    if config_to_dwarf_id_str(dwarf_id) == "3":
        prompt = "Enter the desired wide gain between (0-240):"
    else:
        prompt = "Enter the desired wide gain between (60-160):"
    camera_wide_gain_init = read_camera_wide_gain()
    camera_wide_gain = input(f"{prompt}[{camera_wide_gain_init}]:") if camera_wide_gain_init else input(prompt+"[80]")
    if not camera_wide_gain and not camera_wide_gain_init:
        if config_to_dwarf_id_str(dwarf_id) == "3":
            camera_wide_gain = "0"
        else:
            camera_wide_gain = "60"
        print("Set to Default:", camera_wide_gain)
    elif config_to_dwarf_id_str(dwarf_id) == "3" and camera_wide_gain and (int(camera_wide_gain)<0 or int(camera_wide_gain) > 240):
        print("Input Data Error:", camera_wide_gain)
        camera_wide_gain = "0"
        print("Set to Default:", camera_wide_gain)
    elif config_to_dwarf_id_str(dwarf_id) == "2" and camera_wide_gain and (int(camera_wide_gain)<60 or int(camera_wide_gain) > 160):
        print("Input Data Error:", camera_wide_gain)
        camera_wide_gain = "60"
        print("Set to Default:", camera_wide_gain)
    elif (camera_wide_gain):
        print("You entered:", camera_wide_gain)
    elif (camera_wide_gain_init):
        camera_wide_gain = camera_wide_gain_init
        print("Saved value used:", camera_wide_gain)
    else:
        print("No value entered:")

    update_cameraconfig(camera_exposure, camera_gain, camera_IR, camera_binning, camera_format, camera_count, camera_wide_exposure, camera_wide_gain)

def read_camera_data():
    print("The values in the Config File are : ")
    print("-----------------------------------")
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = data_config['dwarf_id']
    if (camera_exposure := read_camera_exposure()):
        print("the exposition is: ", camera_exposure)
    if (camera_gain := read_camera_gain()):
        print("the gain is:", camera_gain)
    if (camera_IR := read_camera_IR()):
        if config_to_dwarf_id_str(dwarf_id) == "2":
            if (camera_IR == "0") :
                print("the IR value is: IRCut")
            else:
                print("the IR value is: IRPass")
        else:
            if (camera_IR == "0") :
                print("the IR value is: VIS")
            elif (camera_IR == "1") :
                print("the IR value is: ASTRO")
            else:
                print("the IR value is: DUAL-BAND")
    if (camera_binning := read_camera_binning()):
        if (camera_binning == "0"):
            print("the Binning value is 4k")
        else:
            print("the Binning value is 2k")
    if (camera_format := read_camera_format()):
        if (camera_format == "0"):
            print("the image format value is: FITS")
        else:
            print("the image format value is: TIFF")
    if (camera_count := read_camera_count()):
        print("the number of images for the session is:", camera_count)
    if (camera_wide_exposure := read_camera_wide_exposure()):
        print("the wide exposition is: ", camera_wide_exposure)
    if (camera_wide_gain := read_camera_wide_gain()):
        print("the wide gain is:", camera_wide_gain)

def input_bluetooth_data():
    prompt = "Enter the desired AP wifi type  (0 = 5G (defaut), 1 = 2.4G) "
    ble_wifi_type_init = read_bluetooth_ble_wifi_type()
    ble_wifi_type = input(f"{prompt}[{ble_wifi_type_init}]:") if ble_wifi_type_init else input(prompt+"[0]")
    if not ble_wifi_type and not ble_wifi_type_init:
        ble_wifi_type = "0"
        print("Set to Default:", ble_wifi_type)
    elif ble_wifi_type and (int(ble_wifi_type)<0 or int(ble_wifi_type) > 1):
        print("Input Data Error:", ble_wifi_type)
        ble_wifi_type = "0"
        print("Set to Default:", ble_wifi_type)
    elif (ble_wifi_type):
        print("You entered:", ble_wifi_type)
    elif (ble_wifi_type_init):
        ble_wifi_type = ble_wifi_type_init
        print("Saved value used:", ble_wifi_type)
    else:
        print("No value entered:")

    prompt = "Enter the desired AP auto start  (0 = boot not start (defaut), 1 = boot start) "
    ble_autoAP_init = read_bluetooth_autoAP()
    ble_autoAP = input(f"{prompt}[{ble_autoAP_init}]:") if ble_autoAP_init else input(prompt+"[0]")
    if not ble_autoAP and not ble_autoAP_init:
        ble_autoAP = "0"
        print("Set to Default:", ble_autoAP)
    elif ble_autoAP and (int(ble_autoAP)<0 or int(ble_autoAP) > 1):
        print("Input Data Error:", ble_autoAP)
        ble_autoAP = "0"
        print("Set to Default:", ble_autoAP)
    elif (ble_autoAP):
        print("You entered:", ble_autoAP)
    elif (ble_autoAP_init):
        ble_autoAP = ble_autoAP_init
        print("Saved value used:", ble_autoAP)
    else:
        print("No value entered:")

    prompt = "Enter the desired Contry List config set  (0 = don't configure (defaut), 1 = configure) "
    ble_country_list_init = read_bluetooth_country_list()
    ble_country_list = input(f"{prompt}[{ble_country_list_init}]:") if ble_country_list_init else input(prompt+"[0]")
    if not ble_country_list and not ble_country_list_init:
        ble_country_list = "0"
        print("Set to Default:", ble_country_list)
    elif ble_country_list and (int(ble_country_list)<0 or int(ble_country_list) > 1):
        print("Input Data Error:", ble_country_list)
        ble_country_list = "0"
        print("Set to Default:", ble_country_list)
    elif (ble_country_list):
        print("You entered:", ble_country_list)
    elif (ble_country_list_init):
        ble_country_list = ble_country_list_init
        print("Saved value used:", ble_country_list)
    else:
        print("No value entered:")

    prompt = "Enter the desired Contry "
    ble_country_init = read_bluetooth_country()
    ble_country = input(f"{prompt}[{ble_country_init}]:") if ble_country_init else input(prompt)
    if not ble_country and not ble_country_init:
        ble_country = ""
    elif (ble_country):
        print("You entered:", ble_country)
    elif (ble_country_init):
        ble_country = ble_country_init
        print("Saved value used:", ble_country)
    else:
        print("No value entered:")

    prompt = "Enter the desired ble Password: "
    ble_psd_init = read_bluetooth_ble_psd()
    ble_psd = input(f"{prompt}[{ble_psd_init}]:") if ble_psd_init else input(prompt+"[DWARF_12345678]")
    if not ble_psd and not ble_psd_init:
        ble_psd = "DWARF_12345678"
        print("Set to Default:", ble_psd)
    elif (ble_psd):
        print("You entered:", ble_psd)
    elif (ble_psd_init):
        ble_psd = ble_psd_init
        print("Saved value used:", ble_psd)
    else:
        print("No value entered:")

    prompt = "Enter the desired STA auto start  (0 = boot not start (defaut), 1 = boot start) "
    ble_autoSTA_init = read_bluetooth_autoSTA()
    ble_autoSTA = input(f"{prompt}[{ble_autoSTA_init}]:") if ble_autoSTA_init else input(prompt+"[0]")
    if not ble_autoSTA and not ble_autoSTA_init:
        ble_autoSTA = "0"
        print("Set to Default:", ble_autoSTA)
    elif ble_autoSTA and (int(ble_autoSTA)<0 or int(ble_autoSTA) > 1):
        print("Input Data Error:", ble_autoSTA)
        ble_autoSTA = "0"
        print("Set to Default:", ble_autoSTA)
    elif (ble_autoSTA):
        print("You entered:", ble_autoSTA)
    elif (ble_autoSTA_init):
        ble_autoSTA = ble_autoSTA_init
        print("Saved value used:", ble_autoSTA)
    else:
        print("No value entered:")

    prompt = "Enter the desired STA ssid "
    ble_STA_ssid_init = read_bluetooth_ble_STA_ssid()
    ble_STA_ssid = input(f"{prompt}[{ble_STA_ssid_init}]:") if ble_STA_ssid_init else input(prompt)
    if (ble_STA_ssid):
        print("You entered:", ble_STA_ssid)
    elif (ble_STA_ssid_init):
        ble_STA_ssid = ble_STA_ssid_init
        print("Saved value used:", ble_STA_ssid)
    else:
        print("No value entered:")

    prompt = "Enter the desired STA Password "
    ble_STA_pwd_init = read_bluetooth_ble_STA_pwd()
    ble_STA_pwd = input(f"{prompt}[{ble_STA_pwd_init}]:") if ble_STA_pwd_init else input(prompt)
    if (ble_STA_pwd):
        print("You entered:", ble_STA_pwd)
    elif (ble_STA_pwd_init):
        ble_STA_pwd = ble_STA_pwd_init
        print("Saved value used:", ble_STA_pwd)
    else:
        print("No value entered:")

    update_bluetoothconfig(ble_wifi_type, ble_autoAP, ble_country_list, ble_country, ble_psd, ble_autoSTA, ble_STA_ssid, ble_STA_pwd)
    save_bluetooth_config_from_ini_file()

def read_bluetooth_data():
    print("The values in the Config File are : ")
    print("-----------------------------------")
    if (ble_wifi_type := read_bluetooth_ble_wifi_type()):
        if (ble_wifi_type == "0"):
            print("the AP wifi type is: 5G")
        else:
            print("the AP wifi type is: 2.4G")
    if (ble_autoAP := read_bluetooth_autoAP()):
        if (ble_autoAP == "0"):
            print("the AP auto start value is: boot not start")
        else:
            print("the AP auto start value: boot start")
    if (ble_country_list := read_bluetooth_country_list()):
        if (ble_country_list == "0"):
            print("the Contry List config set value is: don't configure")
        else:
            print("the Contry List config set value: configure")
    if (ble_country := read_bluetooth_country()):
        print("the country is: ", ble_country)
    if (ble_psd := read_bluetooth_ble_psd()):
        print("the ble Password is: ", ble_psd)
    if (ble_autoSTA := read_bluetooth_autoSTA()):
        if (ble_autoSTA == "0"):
            print("the STA auto start value is: boot not start")
        else:
            print("the STA auto start value: boot start")
    if (ble_STA_ssid := read_bluetooth_ble_STA_ssid()):
        print("the STA ssid is: ", ble_STA_ssid)
    if (ble_STA_pwd := read_bluetooth_ble_STA_pwd()):
        print("the STA Password is: ", ble_STA_pwd)

def input_test():
    user_longitude = input("Enter your Longitude: ")
    print("You entered:", user_longitude)
    user_latitude = input("Enter your Latitude: ")
    print("You entered:", user_latitude)
    user_timezone = input("Enter your TimeZone: ")
    print("You entered:", user_timezone)
    print("")
    update_config(user_longitude, user_latitude, user_timezone)

def input_manual_target():
    target_name = input("Enter a name for the target: ")
    print("You entered:", target_name)
    manual_RA = input("Enter the Right Ascension (hr:mm:ss.s) or decimal: ")
    print("You entered:", manual_RA)
    try:
        decimal_RA = float(manual_RA)
    except ValueError:
        decimal_RA = parse_ra_to_float(manual_RA)
    print("Converted to:", decimal_RA)
    manual_declination = input("Enter the Declination (<sign>deg:mm:ss.s) or decimal: ")
    print("You entered:", manual_declination)
    try:
        decimal_Dec = float(manual_declination)
    except ValueError:
        decimal_Dec = parse_ra_to_float(manual_declination)
    print("Converted to:", decimal_Dec)
    print("")
    go_goto = input("Press Enter to continue or 0 to exit: ")
    if (go_goto !="0"):
        # Convert to decimal value if not enterered
        perform_goto(decimal_RA, decimal_Dec, target_name)
    else:
        exit

def input_frame(masked):
    user_frame = input("Enter the wireshark capture frame payload data (option copy as C String) or 0 to return to previous menu: ")
    user_maskedcode = ""
    if (user_frame == "0"):
      return '0'
    else:
      print("You entered:", user_frame)
      if (masked):
          user_maskedcode = input("Enter the masked code: ")
          print("You entered:", user_maskedcode)
      perform_decode_wireshark(user_frame, masked, user_maskedcode)
      input_frame(masked)
      return ''

def select_solar_target (target):
   
    target_name = target
    target_id = None
   
    if (target == "Mercury"):
        target_id = 1

    if (target == "Venus"):
        target_id = 2

    if (target == "Mars"):
        target_id = 3

    if (target == "Jupiter"):
        target_id = 4

    if (target == "Saturn"):
        target_id = 5

    if (target == "Uranus"):
        target_id = 6

    if (target == "Neptune"):
        target_id = 7

    if (target == "moon"):
        target_id = 8

    if (target == "Sun"):
        target_id = 9

    perform_goto_stellar(target_id, target_name)

def update_config(longitude, latitude, timezone):
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Update the value in the CONFIG section
    config['CONFIG']['LONGITUDE'] = longitude
    config['CONFIG']['LATITUDE'] = latitude
    config['CONFIG']['TIMEZONE'] = timezone

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def update_cameraconfig(camera_exposure, camera_gain, camera_IR, camera_binning, camera_format, camera_count, camera_wide_exposure, camera_wide_gain):

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Update the value in the CONFIG section
    if (camera_exposure):
        config['CONFIG']['EXPOSURE'] = camera_exposure
    if (camera_gain):
        config['CONFIG']['GAIN'] = camera_gain
    if (camera_IR):
        config['CONFIG']['IRCUT'] = camera_IR
    if (camera_binning):
        config['CONFIG']['BINNING'] = camera_binning
    if (camera_format):
        config['CONFIG']['FORMAT'] = camera_format
    if (camera_count):
        config['CONFIG']['COUNT'] = camera_count
    if (camera_wide_exposure):
        config['CONFIG']['WIDE_EXPOSURE'] = camera_wide_exposure
    if (camera_wide_gain):
        config['CONFIG']['WIDE_GAIN'] = camera_wide_gain

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def update_bluetoothconfig(ble_wifi_type, ble_autoAP, ble_country_list, ble_country, ble_psd, ble_autoSTA, ble_STA_ssid, ble_STA_pwd):

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Update the value in the CONFIG section
    if (ble_wifi_type):
        config['CONFIG']['BLE_WIFI_TYPE'] = ble_wifi_type
    if (ble_autoAP):
        config['CONFIG']['BLE_AUTO_AP'] = ble_autoAP
    if (ble_country_list):
        config['CONFIG']['BLE_COUNTRY_LIST'] = ble_country_list
    if (ble_country):
        config['CONFIG']['BLE_COUNTRY'] = ble_country
    if (ble_psd):
        config['CONFIG']['BLE_PSD'] = ble_psd
    if (ble_autoSTA):
        config['CONFIG']['BLE_AUTO_STA'] = ble_autoSTA
    if (ble_STA_ssid):
        config['CONFIG']['BLE_STA_SSID'] = ble_STA_ssid
    if (ble_STA_pwd):
        config['CONFIG']['BLE_STA_PWD'] = ble_STA_pwd

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def perform_goto_target(target):
    ra = None
    dec = None

    if (target == "Polaris"):
        ra = 2.5390302777777776;
        dec = 89.26980527777778;

    if (target == "Vega"):
        ra = 18.61522686111111;
        dec = 38.784415833333334;

    if (target == "M42"):
        ra = 5.588475138888889;
        dec = -5.3923;

    if (target == "M31"):
        ra = 0.7122101388888887;
        dec = 41.271721388888885;

    if (ra):
        return perform_goto(ra, dec, target)

    print(f"Error: Data for Target: {target} Not Found")

def choice_test():
    while True:
        display_menu_test()
        user_choice = get_user_choice_test().upper()

        if user_choice == 'T1':
            option_20()

        elif user_choice == 'T2':
            option_21()

        elif user_choice == 'T3':
            option_22()

        elif user_choice == 'T4':
            option_23()

        elif user_choice == 'D':
            if (option_24() == '0'):
              break

        elif user_choice == '0':
            print("Return to the main menu")
            break

        else:
            print("Invalid choice. Please enter a correct value.")

def choice_camera():
    while True:
        display_menu_camera()
        user_choice = get_user_choice_camera().upper()

        if user_choice == 'C1':
            option_C1()

        elif user_choice == 'C2':
            option_C2()

        elif user_choice == 'C3':
            option_C3()

        elif user_choice == 'C4':
            option_C4()

        elif user_choice == 'CT4':
            option_CT4()

        elif user_choice == 'CW4':
            option_CW4()

        elif user_choice == 'C5':
            option_C5()

        elif user_choice == 'C6':
            option_C6()

        elif user_choice == 'C7':
            option_C7()

        elif user_choice == 'C8':
            option_C8()

        elif user_choice == 'C9':
            option_C9()

        elif user_choice == 'C10':
            option_C10()

        elif user_choice == 'C11':
            option_C11()

        elif user_choice == 'C12':
            option_C12()

        elif user_choice == 'C13':
            option_C13()

        elif user_choice == 'C14':
            option_C14()

        elif user_choice == 'C15':
            option_C15()

        elif user_choice == 'C16':
            option_C16()

        elif user_choice == '0':
            print("Return to the main menu")
            break

        else:
            print("Invalid choice. Please enter a correct value.")

def choice_bluetooth():
    while True:
        display_menu_bluetooth()
        user_choice = get_user_choice_bluetooth().upper()

        if user_choice == 'C':
            option_BC()

        elif user_choice == 'CD':
            option_BCD()

        elif user_choice == 'CW':
            option_BCW()

        elif user_choice == 'R':
            option_BR()

        elif user_choice == 'S':
            option_BS()

        elif user_choice == '0':
            print("Return to the main menu")
            break

        else:
            print("Invalid choice. Please enter a correct value.")

def choice_motor():
    while True:
        display_menu_motor()
        user_choice = get_user_choice_motor().upper()

        if user_choice == 'C':
            option_MC()

        elif user_choice == 'I':
            option_MI()

        elif user_choice == 'I3':
            option_MI3()

        elif user_choice == 'P':
            option_MP()

        elif user_choice == 'P3':
            option_MP3()

        elif user_choice == 'S':
            option_MS()

        elif user_choice == 'S3':
            option_MS3()

        elif user_choice == 'RR':
            option_RR()

        elif user_choice == 'RS':
            option_RS()

        elif user_choice == 'GP':
            option_GP()

        elif user_choice == 'PA':
            option_PA()

        elif user_choice == 'PS':
            option_PS()

        elif user_choice == '0':
            print("Return to the main menu")
            break

        else:
            print("Invalid choice. Please enter a correct value.")

def main():
    while True:
        display_menu()
        try:
            user_choice = get_user_choice().upper()
        except KeyboardInterrupt:
            my_logger.warning("Operation interrupted by the user (CTRL+C).")
            user_choice = '0'

        if user_choice == '1':
            option_1()

        elif user_choice == '2':
            option_2()

        elif user_choice == '3':
            option_3()

        elif user_choice == '4':
            option_4()

        elif user_choice == '5':
            option_5()

        elif user_choice == '6':
            option_6()

        elif user_choice == '7':
            option_7()

        elif user_choice == '8':
            option_8()

        elif user_choice == '9':
            option_9()

        elif user_choice == '10':
            option_10()

        elif user_choice == '11':
            option_11()

        elif user_choice == '12':
            option_12()

        elif user_choice == 'B':
            option_B()

        elif user_choice == 'C':
            option_C()

        elif user_choice == 'D':
            option_D()

        elif user_choice == 'L':
            option_L()

        elif user_choice == 'M':
            option_M()

        elif user_choice == 'S':
            option_S()

        elif user_choice == 'T':
            option_T()

        elif user_choice == 'R':
            option_R()

        elif user_choice == 'P':
            option_P()

        elif user_choice == '0':
            perform_disconnect()
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a correct_value.")

if __name__ == "__main__":
    main()
