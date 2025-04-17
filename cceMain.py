#import xlsxwriter
import tkinter as tk
from tkinter import ttk
import random

# Define constants
RG_SCH_D = 65537
RG_SCH_A0 = 39827
RG_SCH_A1 = 39829
RG_SCH_A2 = 39839
RG_SCH_NUM_REG_IN_ONE_CCE = 6
y_values = []
#cce2RegBndlMapIntrLvd = []
# Fill different colors in different iterations of the loop
colors = ["#FF0000", "#00FF00", "#0000FF", "#F00FFF"]
cs_id = 1
ue_id = 17021
mu = 0
#slot =5
box_width = 40
box_height = 40
pci = 26
nCI = 0


class TestCase:
    def __init__(self,aggrLvl, ue_id, cs1, slot,coreSet0_aggrLvl, numCce, numCceRedCapUe, coreSet0_numCce,cceStart):
        self.aggrLvl = aggrLvl
        self.numCce = numCce
        self.numCceRedCapUe = numCceRedCapUe
        self.coreSet0_numCce = coreSet0_numCce
        self.cceStart = cceStart
        self.coreSet0_aggrLvl = coreSet0_aggrLvl
        self.ue_id= ue_id
        self.cs1 = cs1
        self.slot = slot

def test_case_5MHz(aggregation_level, ue_id, cs1_type,slot,coreSet0_aggrLvl):
    return TestCase(int(aggregation_level), int(ue_id), int(cs1_type),int (slot),int (coreSet0_aggrLvl),8, 0, 8, 0)

def test_case_10MHz(aggregation_level, ue_id,cs1_type,slot,coreSet0_aggrLvl):
    return TestCase(int(aggregation_level), int(ue_id), int(cs1_type),int (slot),int (coreSet0_aggrLvl),16, 8, 16, 1)

def test_case_15MHz(aggregation_level, ue_id,cs1_type,slot,coreSet0_aggrLvl):
    return TestCase(int(aggregation_level), int(ue_id), int(cs1_type),int (slot),int (coreSet0_aggrLvl),12, 8, 16, 2)
    
def test_case_20MHz(aggregation_level, ue_id,cs1_type,slot,coreSet0_aggrLvl):
    return TestCase(int(aggregation_level), int(ue_id), int(cs1_type),int (slot),int (coreSet0_aggrLvl),17, 8, 16, 0)

def test_case_25MHz(aggregation_level, ue_id,cs1_type,slot,coreSet0_aggrLvl):
    return TestCase(int(aggregation_level), int(ue_id), int(cs1_type),int (slot),int (coreSet0_aggrLvl),22, 16, 16, 2)

def test_case_100MHz(aggregation_level, ue_id,cs1_type,slot,coreSet0_aggrLvl):
    return TestCase(int(aggregation_level), int(ue_id), int(cs1_type),int (slot),int (coreSet0_aggrLvl),90, 16, 16, 21)


def generate_random_ue_id():
    return random.randint(16921, 16921 + 1536)



def rg_sch_utl_cal_y(cs_id, prev_y):
    if cs_id == 0:
        return (RG_SCH_A0 * prev_y) % RG_SCH_D
    elif cs_id == 1:
        return (RG_SCH_A1 * prev_y) % RG_SCH_D
    else:
        return (RG_SCH_A2 * prev_y) % RG_SCH_D

def rg_sch_lvl1_utl_upd_y(cs_id, ue_id, mu):
    num_of_slots_per_radio_frame = (1 << mu) * 10
   
    temp_y = ue_id
    y_values = []
    for i in range(num_of_slots_per_radio_frame):
        y = rg_sch_utl_cal_y(cs_id, temp_y)
        y_values.append(y)
        temp_y = y
        print("slot: ", i,"Y: ",y)
    return y_values

def rg_sch_lvl1_utl_get_y(slot):
    ssPeriodicity =10  
    return y_values[slot]



def rgSCHCfgInterLeavedCs(numCce,cce2RegBndlMapIntrLvd, shiftIdx):
    R = 2
    L = 6
    numRegCs = numCce * RG_SCH_NUM_REG_IN_ONE_CCE
    nShift = shiftIdx

    C = numRegCs // (L * R)

    for c in range(C):
        for r in range(R):
            x = c * R + r
            fInterleaverx = ((r * C) + c + nShift) % (numRegCs // L)
            print(f"rgSCHCfgInterLeavedCs: nShift = {nShift}, numRegCs = {numRegCs}, L = {L}, R = {R}, C = {C}, c = {c}, r = {r}, x = {x}, Interleaver output = {fInterleaverx}")
            cce2RegBndlMapIntrLvd[x] = fInterleaverx

def getInterLeavedCs(cceIdx,cce2RegBndlMapIntrLvd):
    return cce2RegBndlMapIntrLvd[cceIdx]

def create_boxes(test_case):
    # Calculate result
    #numCandidts=1
    # Create a list to store the boxes
    boxes0 = []
    y_coreset0=0
    cce2RegBndlMapIntrLvd = [0] * 100
    canvas.delete("all")
    # Create the boxes
    canvas.create_text(160, 10, text=f"Coreset0", anchor=tk.NW)
 #Coreset 0 
    rgSCHCfgInterLeavedCs(test_case.coreSet0_numCce, cce2RegBndlMapIntrLvd,pci)
    for i in range(test_case.coreSet0_numCce):
        x = i * box_width+test_case.cceStart*box_width
        y= 50
        box = canvas.create_rectangle(x, y, x+box_width, y+box_height, fill="#FFFFFF")
        boxes0.append(box)
        canvas.create_text(x+20, y+20, text=str(i))
    if (test_case.coreSet0_aggrLvl == 8):
        numCandidts = 2
    elif (test_case.coreSet0_aggrLvl == 4):
        numCandidts = 2
    elif (test_case.coreSet0_aggrLvl == 2):
        numCandidts = 4
    elif (test_case.coreSet0_aggrLvl == 1):
        numCandidts = 4
    for i in range(numCandidts):
        csLoc = int((y_coreset0 + ((i * test_case.coreSet0_numCce) // (test_case.coreSet0_aggrLvl * numCandidts)) + nCI) % (test_case.coreSet0_numCce // test_case.coreSet0_aggrLvl))
        startCceIdx = csLoc * test_case.coreSet0_aggrLvl
 #       mappedCsLoc = getInterLeavedCs(startCceIdx)
        mappedCsLoc = cce2RegBndlMapIntrLvd[startCceIdx]
        #mappedCsLoc = startCceIdx
        print("csLoc,startCceIdx,mappedCsLoc",csLoc,startCceIdx,mappedCsLoc)
        # Color the boxes starting from csLoc
        for j in range(startCceIdx, startCceIdx + test_case.coreSet0_aggrLvl):
          #  mappedCsLoc = getInterLeavedCs(j)
            print("j, mappedCsLoc", j,cce2RegBndlMapIntrLvd[j])
            mappedCsLoc = cce2RegBndlMapIntrLvd[j]
            #mappedCsLoc = j
            canvas.itemconfig(boxes0[mappedCsLoc], fill=colors[i % len(colors)])
       
    
 #Coreset1
    

  
    for seq in range(1):

        boxes = []  # Initialize the boxes array for normal UE
        boxes1 = [] # Initialize boxes1 array for RedCap UE
        y_value = []
        y_value = rg_sch_lvl1_utl_upd_y(cs_id, test_case.ue_id+ seq, mu)
        y_val = y_value[test_case.slot]
        y_value_redcap = []
        y_value_redcap = rg_sch_lvl1_utl_upd_y(cs_id, test_case.ue_id+1+ seq, mu)
        y_val_redcap = y_value_redcap[test_case.slot]
        print("RedCap UeIdx,y_val,slot", test_case.ue_id+1,y_val_redcap,test_case.slot)
        print("Normal UeIdx,y_val,slot", test_case.ue_id,y_val,test_case.slot)
      #  cce2RegBndlMapIntrLvd = [0] * test_case.numCce
        cce2RegBndlMapIntrLvd = [0] * 100
        if (test_case.aggrLvl == 8):
            numCandidts = 2
        elif (test_case.aggrLvl == 4):
            numCandidts = 2
        elif (test_case.aggrLvl == 2):
            numCandidts = 4
        elif (test_case.aggrLvl == 1):
            numCandidts = 4
        if (test_case.cs1):       
            # RedCap UE
            shiftIdx = (pci + test_case.cceStart) % test_case.numCceRedCapUe
            rgSCHCfgInterLeavedCs(test_case.numCceRedCapUe,cce2RegBndlMapIntrLvd,shiftIdx)
            canvas.create_text(260, seq*2*box_height+2.5*box_height, text=f"Coreset1 redCapUe- {test_case.ue_id+1+2*seq}", anchor=tk.NW)
            for i in range(test_case.numCceRedCapUe):
                x = i * (box_width)+test_case.cceStart*box_width
                y = seq * 2 * box_height+ 3*box_height
                box = canvas.create_rectangle(x, y, x+box_width, y+box_height, fill="#FFFFFF")
                boxes1.append(box)
                canvas.create_text(x+20, y+20, text=str(i))
                               
            print("RedCapUE UeIdx: ",test_case.ue_id+1, "shiftIdx:" , shiftIdx) 
            for i in range(numCandidts):
                csLoc = int((y_val_redcap + ((i * test_case.numCceRedCapUe) // (test_case.aggrLvl * numCandidts)) + nCI) % (test_case.numCceRedCapUe // test_case.aggrLvl))
                startCceIdx = csLoc * test_case.aggrLvl
                mappedCsLoc = cce2RegBndlMapIntrLvd[startCceIdx]
                print("REDCAP y,csLoc,startCceIdx,mappedCsLoc",y_val_redcap,csLoc,startCceIdx,mappedCsLoc)
                # Color the boxes starting from csLoc
                for j in range(startCceIdx, (startCceIdx + test_case.aggrLvl)):
                    mappedCsLoc = cce2RegBndlMapIntrLvd[j]
                    print("i,j,mappedCsLoc",i,j,mappedCsLoc)
                    canvas.itemconfig(boxes1[mappedCsLoc], fill=colors[i % len(colors)])
            
            # Normal UE
            shiftIdx = (pci + test_case.cceStart) % test_case.numCce
            rgSCHCfgInterLeavedCs(test_case.numCce,cce2RegBndlMapIntrLvd,shiftIdx)
            canvas.create_text(260, seq*2*box_height+2.5*box_height+2.5*box_height, text=f"Coreset1 RNTI- {test_case.ue_id+2*seq}", anchor=tk.NW)
            for i in range(test_case.numCce):
                x = i * (box_width)
                y = seq * 2 * box_height+ 5*box_height
                box = canvas.create_rectangle(x, y, x+box_width, y+box_height, fill="#FFFFFF")
                boxes.append(box)
                canvas.create_text(x+20, y+20, text=str(i))
                               
            print("UeIdx, shiftIdx", test_case.ue_id, shiftIdx) 
            for i in range(numCandidts):
                csLoc = int((y_val + ((i * test_case.numCce) // (test_case.aggrLvl * numCandidts)) + nCI) % (test_case.numCce // test_case.aggrLvl))
                startCceIdx = csLoc * test_case.aggrLvl
                mappedCsLoc = cce2RegBndlMapIntrLvd[startCceIdx]
                print("y,csLoc,startCceIdx,mappedCsLoc",y_val,csLoc,startCceIdx,mappedCsLoc)
                # Color the boxes starting from csLoc
                for j in range(startCceIdx, (startCceIdx + test_case.aggrLvl)):
                    mappedCsLoc = cce2RegBndlMapIntrLvd[j]
                    print("i,j,mappedCsLoc",i,j,mappedCsLoc)
                    canvas.itemconfig(boxes[mappedCsLoc], fill=colors[i % len(colors)])
                 
        else:
            # redCap
            canvas.create_text(260, seq*2*box_height+2.5*box_height, text=f"Coreset1 redCapUe {test_case.ue_id+1+2*seq}", anchor=tk.NW)
            for i in range(test_case.numCceRedCapUe):
                x = i * (box_width)+test_case.cceStart*box_width
                y = seq * 2 * box_height+ 3*box_height
                box = canvas.create_rectangle(x, y, x+box_width, y+box_height, fill="#FFFFFF")
                boxes1.append(box)
                canvas.create_text(x+20, y+20, text=str(i))
            for i in range(numCandidts):
                csLoc = int((y_val_redcap + ((i * test_case.numCceRedCapUe) // (test_case.aggrLvl * numCandidts)) + nCI) % (test_case.numCceRedCapUe // test_case.aggrLvl))
                startCceIdx = csLoc * test_case.aggrLvl
                #mappedCsLoc = cce2RegBndlMapIntrLvd[startCceIdx]
                mappedCsLoc = startCceIdx
                print("y,csLoc,startCceIdx,mappedCsLoc",y_val_redcap,csLoc,startCceIdx,mappedCsLoc)
                # Color the boxes starting from csLoc
                for j in range(startCceIdx, startCceIdx + test_case.aggrLvl):
                    #mappedCsLoc = cce2RegBndlMapIntrLvd[j]
                    mappedCsLoc = j
                    #print("i,j,mappedCsLoc",i,j,mappedCsLoc)
                    canvas.itemconfig(boxes1[mappedCsLoc], fill=colors[i % len(colors)])
            # Normal UE
            canvas.create_text(260, seq*2*box_height+2.5*box_height+2*box_height, text=f"Coreset1 RNTI- {test_case.ue_id+2*seq}", anchor=tk.NW)
            for i in range(test_case.numCce):
                x = i * (box_width)
                y = seq * 2 * box_height+ 5*box_height
                box = canvas.create_rectangle(x, y, x+box_width, y+box_height, fill="#FFFFFF")
                boxes.append(box)
                canvas.create_text(x+20, y+20, text=str(i))
            for i in range(numCandidts):
                csLoc = int((y_val + ((i * test_case.numCce) // (test_case.aggrLvl * numCandidts)) + nCI) % (test_case.numCce // test_case.aggrLvl))
                startCceIdx = csLoc * test_case.aggrLvl
                #mappedCsLoc = cce2RegBndlMapIntrLvd[startCceIdx]
                mappedCsLoc = startCceIdx
                print("y,csLoc,startCceIdx,mappedCsLoc",y_val,csLoc,startCceIdx,mappedCsLoc)
                # Color the boxes starting from csLoc
                for j in range(startCceIdx, startCceIdx + test_case.aggrLvl):
                    #mappedCsLoc = cce2RegBndlMapIntrLvd[j]
                    mappedCsLoc = j
                    #print("i,j,mappedCsLoc",i,j,mappedCsLoc)
                    canvas.itemconfig(boxes[mappedCsLoc], fill=colors[i % len(colors)])
    canvas.update()  # Update the canvas
    canvas.after(1000)  # Wait for 1 second before clearing the canvas



def execute_test_case(test_case_var, aggregation_var,ue_id_entry,cs1_var,slot_var,coreSet0_aggrLvl_var):
    test_case_name = test_case_var.get()
    aggregation_level = aggregation_var.get()
    ue_id_text = ue_id_entry.get()
    cs1_type_str = cs1_var.get()
    if (cs1_type_str == "Interleaved"):
        cs1_type = 1
    elif (cs1_type_str == "Non-Interleaved"):
        cs1_type = 0
    slot = slot_var.get()
    coreSet0_aggrLvl = coreSet0_aggrLvl_var.get()
    
    # Validate UeId
    try:
        ue_id = int(ue_id_text)
        if not (16921 <= ue_id <= 16921 + 1536):
            print("UeId is out of range")
            return
    except ValueError:
        print("Invalid UeId. It must be an integer.")
        return
    
    if test_case_name == "5MHz":
        test_case = test_case_5MHz(aggregation_level, ue_id, cs1_type,slot,coreSet0_aggrLvl)
    elif test_case_name == "10MHz":
        test_case = test_case_10MHz(aggregation_level, ue_id, cs1_type,slot,coreSet0_aggrLvl)
    elif test_case_name == "15MHz":
        test_case = test_case_15MHz(aggregation_level, ue_id, cs1_type,slot,coreSet0_aggrLvl)
    elif test_case_name == "20MHz":
        test_case = test_case_20MHz(aggregation_level, ue_id, cs1_type,slot,coreSet0_aggrLvl)
    elif test_case_name == "25MHz":
        test_case = test_case_25MHz(aggregation_level, ue_id, cs1_type,slot,coreSet0_aggrLvl)
    elif test_case_name == "100MHz":
        test_case = test_case_100MHz(aggregation_level, ue_id, cs1_type,slot,coreSet0_aggrLvl)
    else:
        print("Invalid test case name")

    create_boxes(test_case)

root = tk.Tk()
root.title("Box Series")

# Label and dropdown for test case
label = tk.Label(root, text="Select test case:")
label.pack()

test_case_var = tk.StringVar()
test_case_menu = ttk.Combobox(root, textvariable=test_case_var)
test_case_menu['values'] = ("5MHz", "10MHz","15MHz", "20MHz","25MHz", "100MHz")
test_case_menu.current(1)
test_case_menu.pack()

# Label and dropdown for CORESET-0 aggregation level selection
label_aggregation = tk.Label(root, text="Select CORESET-0 aggregation level:")
label_aggregation.pack()
coreSet0_aggrLvl_var = tk.StringVar()
coreSet0_aggrLvl_menu = ttk.Combobox(root, textvariable=coreSet0_aggrLvl_var)
coreSet0_aggrLvl_menu['values'] = ("1", "2", "4", "8")
coreSet0_aggrLvl_menu.current(1)
coreSet0_aggrLvl_menu.pack()

# Label and dropdown for CORESET-1 aggregation level selection
label_aggregation = tk.Label(root, text="Select CORESET-1 aggregation level:")
label_aggregation.pack()

aggregation_var = tk.StringVar()
aggregation_menu = ttk.Combobox(root, textvariable=aggregation_var)
aggregation_menu['values'] = ("1", "2", "4", "8")
aggregation_menu.current(2)
aggregation_menu.pack()


# Label and dropdown for interleaved/non-interleaved coreset-1
label_intlvd_cs1 = tk.Label(root, text="Coreset-1:")
label_intlvd_cs1.pack()

cs1_var = tk.StringVar()
cs1_menu = ttk.Combobox(root, textvariable=cs1_var)
cs1_menu['values'] = ("Interleaved", "Non-Interleaved")
cs1_menu.current(1)
cs1_menu.pack()


# Label and dropdown for slot number
label_slot = tk.Label(root, text="Slot no")
label_slot.pack()

slot_var = tk.StringVar()
slot_menu = ttk.Combobox(root, textvariable=slot_var)
slot_menu['values'] = ("0", "1", "2", "3","4","5","6","7", "8","9")
slot_menu.current(0)
slot_menu.pack()


# Label and entry for UeId input
label_ue_id = tk.Label(root, text="Enter UeId (or leave empty for random):")
label_ue_id.pack()

ue_id_entry = tk.Entry(root)
ue_id_entry.pack()


# Button to generate random UeId
def set_random_ue_id():
    random_ue_id = generate_random_ue_id()
    ue_id_entry.delete(0, tk.END)
    ue_id_entry.insert(0, str(random_ue_id))

random_ue_id_button = tk.Button(root, text="Generate Random UeId", command=set_random_ue_id)
random_ue_id_button.pack()


# Execute button
button = tk.Button(root, text="Execute", command=lambda: execute_test_case(test_case_var, aggregation_var, ue_id_entry,cs1_var,slot_var,coreSet0_aggrLvl_var))
button.pack()
# Create a canvas to draw the boxes
canvas = tk.Canvas(root, width=800, height=600, scrollregion=(0, 0, 4000, 1500))
canvas.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH, expand=True)

# Create horizontal and vertical scrollbars
hscrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

vscrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Configure the canvas to use the scrollbars
canvas.config(xscrollcommand=hscrollbar.set, yscrollcommand=vscrollbar.set)
hscrollbar.config(command=canvas.xview)
vscrollbar.config(command=canvas.yview)




root.mainloop()




