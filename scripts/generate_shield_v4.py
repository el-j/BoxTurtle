import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_shield_project_v4():
    root = ET.Element("module", fritzingVersion="0.9.3b")
    
    instances = ET.SubElement(root, "instances")
    
    # --- Helper for Placement ---
    def add_part(id, moduleId, path, x, y):
        inst = ET.SubElement(instances, "instance", moduleIdRef=moduleId, modelIndex=id, path=path)
        views = ET.SubElement(inst, "views")
        pcb = ET.SubElement(views, "pcbView", layer="copper1")
        ET.SubElement(pcb, "geometry", z="5.5", x=str(x), y=str(y))
        ET.SubElement(views, "schematicView", layer="schematic")
        ET.SubElement(views, "breadboardView", layer="breadboard")

    # --- Components ---
    
    # 1. PCB Outline (100mm x 90mm)
    add_part("PCB1", "RectanglePCBModuleID", "RectanglePCBModuleID", 0, 0)

    # 2. MCU: Pico (Center)
    add_part("MCU1", "Raspberry-Pi-Pico-v1", "Raspberry-Pi-Pico-v1.fzp", 400, 350)

    # 3. Stepper Drivers (Flanking)
    add_part("Driver1", "Pololu_A4988", "Pololu_A4988.fzp", 150, 250)
    add_part("Driver2", "Pololu_A4988", "Pololu_A4988.fzp", 150, 550)
    add_part("Driver3", "Pololu_A4988", "Pololu_A4988.fzp", 650, 250)
    add_part("Driver4", "Pololu_A4988", "Pololu_A4988.fzp", 650, 550)

    # 4. Motor Connectors (NEMA 14)
    add_part("NEMA14_L1", "GenericFemaleHeader_4pin", "GenericFemaleHeader_4pin.fzp", 50, 250)
    add_part("NEMA14_L2", "GenericFemaleHeader_4pin", "GenericFemaleHeader_4pin.fzp", 50, 550)
    add_part("NEMA14_L3", "GenericFemaleHeader_4pin", "GenericFemaleHeader_4pin.fzp", 850, 250)
    add_part("NEMA14_L4", "GenericFemaleHeader_4pin", "GenericFemaleHeader_4pin.fzp", 850, 550)

    # 5. Sensor Connectors (Omron D2HW)
    add_part("Omron_L1", "GenericFemaleHeader_3pin", "GenericFemaleHeader_3pin.fzp", 200, 800)
    add_part("Omron_L2", "GenericFemaleHeader_3pin", "GenericFemaleHeader_3pin.fzp", 350, 800)
    add_part("Omron_L3", "GenericFemaleHeader_3pin", "GenericFemaleHeader_3pin.fzp", 500, 800)
    add_part("Omron_L4", "GenericFemaleHeader_3pin", "GenericFemaleHeader_3pin.fzp", 650, 800)

    # 6. Servo Connector
    add_part("Servo_Cutter", "GenericFemaleHeader_3pin", "GenericFemaleHeader_3pin.fzp", 800, 800)

    # 7. Power Input & Buck
    add_part("Term_Power", "ScrewTerminal_2pin", "ScrewTerminal_2pin.fzp", 50, 50)
    add_part("Buck1", "Voltage_Regulator_Module", "Voltage_Regulator_Module.fzp", 200, 50)

    # 8. Expansion
    add_part("I2C_Exp", "GenericFemaleHeader_4pin", "GenericFemaleHeader_4pin.fzp", 450, 50)
    add_part("Aux_Disp", "GenericFemaleHeader_4pin", "GenericFemaleHeader_4pin.fzp", 700, 50)

    # --- NEW: SAFETY & STABILITY COMPONENTS ---
    
    # 9. Electrolytic Capacitors (100uF) for Drivers - CRITICAL for Steppers
    # Placed right next to VMOT pins of drivers
    add_part("Cap_D1", "ElectrolyticCapacitor", "ElectrolyticCapacitor.fzp", 150, 200)
    add_part("Cap_D2", "ElectrolyticCapacitor", "ElectrolyticCapacitor.fzp", 150, 500)
    add_part("Cap_D3", "ElectrolyticCapacitor", "ElectrolyticCapacitor.fzp", 650, 200)
    add_part("Cap_D4", "ElectrolyticCapacitor", "ElectrolyticCapacitor.fzp", 650, 500)

    # 10. I2C Pull-up Resistors (4.7k)
    add_part("R_SDA", "Resistor", "Resistor.fzp", 450, 100)
    add_part("R_SCL", "Resistor", "Resistor.fzp", 480, 100)

    # 11. Power LED + Resistor
    add_part("LED_Pwr", "LED", "LED.fzp", 100, 50)
    add_part("R_LED", "Resistor", "Resistor.fzp", 120, 50)


    # --- Nets ---
    nets = ET.SubElement(root, "nets")
    net_counter = 0
    
    def add_net(name, connections):
        nonlocal net_counter
        net = ET.SubElement(nets, "net", connectorId=f"net{net_counter}", name=name)
        net_counter += 1
        for part_id, pin in connections:
            ET.SubElement(net, "connector", id=pin, name=pin).append(ET.Element("partRef", modelIndex=part_id))

    # --- Pin Mappings ---
    pico_phys = {
        "GP0": "connector0", "GP1": "connector1", "GND_3": "connector2", "GP2": "connector3", "GP3": "connector4",
        "GP4": "connector5", "GP5": "connector6", "GND_8": "connector7", "GP6": "connector8", "GP7": "connector9",
        "GP8": "connector10", "GP9": "connector11", "GND_13": "connector12", "GP10": "connector13", "GP11": "connector14",
        "GP12": "connector15", "GP13": "connector16", "GND_18": "connector17", "GP14": "connector18", "GP15": "connector19",
        "GP16": "connector20", "GP17": "connector21", "GND_23": "connector22", "GP18": "connector23", "GP19": "connector24",
        "GP20": "connector25", "GP21": "connector26", "GND_28": "connector27", "GP22": "connector28",
        "3V3": "connector35", "VSYS": "connector38", "GND_38": "connector37"
    }
    drv = {
        "EN": "connector0", "MS1": "connector1", "MS2": "connector2", "MS3": "connector3",
        "RST": "connector4", "SLP": "connector5", "STEP": "connector6", "DIR": "connector7",
        "GND_LOG": "connector8", "VDD": "connector9", "1B": "connector10", "1A": "connector11",
        "2A": "connector12", "2B": "connector13", "GND_MOT": "connector14", "VMOT": "connector15"
    }
    jst4 = {"1": "connector0", "2": "connector1", "3": "connector2", "4": "connector3"}
    jst3 = {"1": "connector0", "2": "connector1", "3": "connector2"}
    pwr = {"VCC": "connector1", "GND": "connector0"}
    cap = {"POS": "connector1", "NEG": "connector0"} # Electrolytic
    res = {"1": "connector0", "2": "connector1"}
    led = {"A": "connector1", "K": "connector0"}

    # --- Wiring ---

    # Power (24V)
    # Add Capacitors (Positive Leg)
    v24_net = [("Term_Power", pwr["VCC"]), ("Buck1", "connector0")]
    for i in range(1, 5):
        v24_net.append((f"Driver{i}", drv["VMOT"]))
        v24_net.append((f"Cap_D{i}", cap["POS"]))
    add_net("24V", v24_net)
    
    # GND
    gnd_net = [("Term_Power", pwr["GND"]), ("Buck1", "connector1"), ("MCU1", pico_phys["GND_3"]),
               ("Servo_Cutter", jst3["1"]), ("I2C_Exp", jst4["2"]), ("Aux_Disp", jst4["2"]),
               ("LED_Pwr", led["K"])]
    for i in range(1, 5):
        gnd_net.append((f"Driver{i}", drv["GND_MOT"]))
        gnd_net.append((f"Driver{i}", drv["GND_LOG"]))
        gnd_net.append((f"Omron_L{i}", jst3["1"]))
        gnd_net.append((f"Cap_D{i}", cap["NEG"])) # Cap Negative Leg
    add_net("GND", gnd_net)

    # 5V
    add_net("5V", [("Buck1", "connector2"), ("MCU1", pico_phys["VSYS"]), 
                   ("Servo_Cutter", jst3["2"]), ("Aux_Disp", jst4["1"]),
                   ("R_LED", res["1"])]) # Power for LED

    # LED Logic
    add_net("LED_Anode", [("R_LED", res["2"]), ("LED_Pwr", led["A"])])

    # 3.3V
    v33_net = [("MCU1", pico_phys["3V3"]), ("I2C_Exp", jst4["1"]),
               ("R_SDA", res["1"]), ("R_SCL", res["1"])] # Pull-ups
    for i in range(1, 5):
        v33_net.append((f"Driver{i}", drv["VDD"]))
        v33_net.append((f"Omron_L{i}", jst3["2"]))
    add_net("3V3", v33_net)

    # Motor Control (Same as before)
    add_net("L1_STEP", [("MCU1", pico_phys["GP2"]), ("Driver1", drv["STEP"])])
    add_net("L1_DIR",  [("MCU1", pico_phys["GP3"]), ("Driver1", drv["DIR"])])
    add_net("L1_UART", [("MCU1", pico_phys["GP0"])])
    add_net("L1_A", [("Driver1", drv["1A"]), ("NEMA14_L1", jst4["1"])])
    add_net("L1_B", [("Driver1", drv["1B"]), ("NEMA14_L1", jst4["2"])])
    add_net("L1_C", [("Driver1", drv["2A"]), ("NEMA14_L1", jst4["3"])])
    add_net("L1_D", [("Driver1", drv["2B"]), ("NEMA14_L1", jst4["4"])])

    add_net("L2_STEP", [("MCU1", pico_phys["GP4"]), ("Driver2", drv["STEP"])])
    add_net("L2_DIR",  [("MCU1", pico_phys["GP5"]), ("Driver2", drv["DIR"])])
    add_net("L2_UART", [("MCU1", pico_phys["GP1"])])
    add_net("L2_A", [("Driver2", drv["1A"]), ("NEMA14_L2", jst4["1"])])
    add_net("L2_B", [("Driver2", drv["1B"]), ("NEMA14_L2", jst4["2"])])
    add_net("L2_C", [("Driver2", drv["2A"]), ("NEMA14_L2", jst4["3"])])
    add_net("L2_D", [("Driver2", drv["2B"]), ("NEMA14_L2", jst4["4"])])

    add_net("L3_STEP", [("MCU1", pico_phys["GP6"]), ("Driver3", drv["STEP"])])
    add_net("L3_DIR",  [("MCU1", pico_phys["GP7"]), ("Driver3", drv["DIR"])])
    add_net("L3_UART", [("MCU1", pico_phys["GP8"])])
    add_net("L3_A", [("Driver3", drv["1A"]), ("NEMA14_L3", jst4["1"])])
    add_net("L3_B", [("Driver3", drv["1B"]), ("NEMA14_L3", jst4["2"])])
    add_net("L3_C", [("Driver3", drv["2A"]), ("NEMA14_L3", jst4["3"])])
    add_net("L3_D", [("Driver3", drv["2B"]), ("NEMA14_L3", jst4["4"])])

    add_net("L4_STEP", [("MCU1", pico_phys["GP10"]), ("Driver4", drv["STEP"])])
    add_net("L4_DIR",  [("MCU1", pico_phys["GP11"]), ("Driver4", drv["DIR"])])
    add_net("L4_UART", [("MCU1", pico_phys["GP9"])])
    add_net("L4_A", [("Driver4", drv["1A"]), ("NEMA14_L4", jst4["1"])])
    add_net("L4_B", [("Driver4", drv["1B"]), ("NEMA14_L4", jst4["2"])])
    add_net("L4_C", [("Driver4", drv["2A"]), ("NEMA14_L4", jst4["3"])])
    add_net("L4_D", [("Driver4", drv["2B"]), ("NEMA14_L4", jst4["4"])])

    # Sensors
    add_net("S1_Sig", [("Omron_L1", jst3["3"]), ("MCU1", pico_phys["GP16"])])
    add_net("S2_Sig", [("Omron_L2", jst3["3"]), ("MCU1", pico_phys["GP17"])])
    add_net("S3_Sig", [("Omron_L3", jst3["3"]), ("MCU1", pico_phys["GP18"])])
    add_net("S4_Sig", [("Omron_L4", jst3["3"]), ("MCU1", pico_phys["GP19"])])

    # Servo
    add_net("Servo_PWM", [("Servo_Cutter", jst3["3"]), ("MCU1", pico_phys["GP20"])])

    # Enable
    en_net = [("MCU1", pico_phys["GP12"])]
    for i in range(1, 5):
        en_net.append((f"Driver{i}", drv["EN"]))
    add_net("ENABLE", en_net)

    # I2C with Pull-ups
    add_net("I2C_SDA", [("MCU1", pico_phys["GP14"]), ("I2C_Exp", jst4["3"]), ("R_SDA", res["2"])])
    add_net("I2C_SCL", [("MCU1", pico_phys["GP15"]), ("I2C_Exp", jst4["4"]), ("R_SCL", res["2"])])

    # Aux
    add_net("AUX_1", [("MCU1", pico_phys["GP21"]), ("Aux_Disp", jst4["3"])])
    add_net("AUX_2", [("MCU1", pico_phys["GP22"]), ("Aux_Disp", jst4["4"])])

    # Output
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open("/Users/rex-fab-alt/Documents/code/playground/BoxTurtle/BT_Wiring/BoxTurtle_Pico_Shield_v2.fz", "w") as f:
        f.write(xml_str)

if __name__ == "__main__":
    create_shield_project_v4()
