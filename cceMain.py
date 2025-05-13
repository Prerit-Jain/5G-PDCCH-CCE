#import xlsxwriter
import tkinter as tk
from tkinter import ttk
import random

# Define constants
SCH_D = 65537
SCH_A0 = 39827
SCH_A1 = 39829
SCH_A2 = 39839
SCH_NUM_REG_IN_ONE_CCE = 6
#y_values = []
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

rbMap = {
    "5MHz": 25,
    "10MHz": 52,
    "15MHz": 79,
    "20MHz": 106,
    "25MHz": 133,
    "100MHz": 273
}

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


def generate_random_ue_id():
    random_id = random.randint(16921, 16921 + 1536)
    ue_id_entry.delete(0, tk.END)
    ue_id_entry.insert(0, str(random_id))



def sch_utl_cal_y(cs_id, prev_y):
    if cs_id == 0:
        return (SCH_A0 * prev_y) % SCH_D
    elif cs_id == 1:
        return (SCH_A1 * prev_y) % SCH_D
    else:
        return (SCH_A2 * prev_y) % SCH_D

def sch_lvl1_utl_upd_y(cs_id, ue_id, mu):
    num_of_slots_per_radio_frame = (1 << mu) * 10
   
    temp_y = ue_id
    y_values = []
    for i in range(num_of_slots_per_radio_frame):
        y = sch_utl_cal_y(cs_id, temp_y)
        y_values.append(y)
        temp_y = y
   #     print("slot: ", i,"Y: ",y)
    return y_values

def sch_lvl1_utl_get_y(slot):
    ssPeriodicity =10  
    return y_values[slot]



def SCHCfgInterLeavedCs(numCce,cce2RegBndlMapIntrLvd, shiftIdx):
    R = 2
    L = 6
    numRegCs = numCce * SCH_NUM_REG_IN_ONE_CCE
    nShift = shiftIdx

    C = numRegCs // (L * R)

    for c in range(C):
        for r in range(R):
            x = c * R + r
            fInterleaverx = ((r * C) + c + nShift) % (numRegCs // L)
            print(f"SCHCfgInterLeavedCs: nShift = {nShift}, numRegCs = {numRegCs}, L = {L}, R = {R}, C = {C}, c = {c}, r = {r}, x = {x}, Interleaver output = {fInterleaverx}")
            cce2RegBndlMapIntrLvd[x] = int(fInterleaverx)

def getInterLeavedCs(cceIdx,cce2RegBndlMapIntrLvd):
    return cce2RegBndlMapIntrLvd[cceIdx]

def draw_coreset(canvas, test_case, colors, x_offset, y_offset, num_cce, label):
    boxes = []
    canvas.create_text(10, y_offset, text=label, anchor=tk.NW, font=("Helvetica", 12, "bold"))
    for i in range(num_cce):
        x = i * box_width + x_offset * box_width+ 110
        if i==0:
            y =y_offset - 15
            canvas.create_text(x, y, text=f"cceStart-{x_offset}", anchor=tk.NW)
        y = y_offset
        box = canvas.create_rectangle(x, y, x + box_width, y + box_height, fill="#FFFFFF")
        boxes.append(box)
        canvas.create_text(x + 20, y + 20, text=str(i))
    return boxes

def create_boxes(test_case):
    # Calculate result
    #numCandidts=1
    # Create a list to store the boxes
    #boxes0 = []
    y_coreset0=0
    cce2RegBndlMapIntrLvd = [0] * 100
    canvas.delete("all")
    # Create the boxes
  #  canvas.create_text(160, 10, text=f"Coreset0", anchor=tk.NW)
    print("Cs1 string", test_case.cs1)
 #Coreset 0 
    SCHCfgInterLeavedCs(test_case.coreSet0_numCce, cce2RegBndlMapIntrLvd,pci)
    boxes = draw_coreset(canvas, test_case, colors, test_case.cceStart, 50, test_case.coreSet0_numCce , "Coreset0")
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
            canvas.itemconfig(boxes[mappedCsLoc], fill=colors[i % len(colors)])
       
    
 #Coreset1
  
    for seq in range(1):

    #    boxes = []  # Initialize the boxes array for normal UE
    #    boxes1 = [] # Initialize boxes1 array for RedCap UE
        y_value = []
        y_value = sch_lvl1_utl_upd_y(cs_id, test_case.ue_id+ seq, mu)
        y_val = y_value[test_case.slot]
        y_value_redcap = []
        y_value_redcap = sch_lvl1_utl_upd_y(cs_id, test_case.ue_id+1+ seq, mu)
        y_val_redcap = y_value_redcap[test_case.slot]
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
        if (test_case.cs1 == "Interleaved"):       
            # Normal UE
            shiftIdx = (pci + test_case.cceStart) % test_case.numCce
            SCHCfgInterLeavedCs(test_case.numCce,cce2RegBndlMapIntrLvd,shiftIdx)
            boxes = draw_coreset(canvas, test_case, colors,0, seq  * box_height+ 3*box_height, test_case.numCce,  f"Coreset1\n RNTI-{test_case.ue_id+2*seq}")               
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
            # Normal UE
            boxes = draw_coreset(canvas, test_case, colors,0, seq * box_height+ 3*box_height, test_case.numCce, f"Coreset1\n RNTI-{test_case.ue_id+2*seq}") 
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



def execute_test_case(test_case_var, aggregation_var,ue_id_entry,cs1_var,slot_var,coreSet0_aggrLvl_var,pdcch_symbol_entry, start_rb_entry):
    test_case_name = test_case_var.get()
    aggregation_level = int(aggregation_var.get())
    ue_id_text = ue_id_entry.get()
    cs1_type_str = cs1_var.get()
    if (cs1_type_str == "Interleaved"):
        cs1_type = 1
    elif (cs1_type_str == "Non-Interleaved"):
        cs1_type = 0
    print("cs1_type",cs1_type)
    slot = int(slot_var.get())
    coreSet0_aggrLvl = int(coreSet0_aggrLvl_var.get())
    start_rb = int(start_rb_entry.get())
    pdcch_symbol_count = int(pdcch_symbol_entry.get())

    # Validate UeId
    try:
        ue_id = int(ue_id_text)
        if not (16921 <= ue_id <= 16921 + 1536):
            print("UeId is out of range")
            return
    except ValueError:
        print("Invalid UeId. It must be an integer.")
        return
    cceCnt = int ((rbMap[test_case_name] * pdcch_symbol_count)/SCH_NUM_REG_IN_ONE_CCE)
    print("cceCnt", cceCnt)
    cceStart = int((start_rb * pdcch_symbol_count)/SCH_NUM_REG_IN_ONE_CCE)
    if test_case_name == "5MHz":
        test_case = TestCase(aggregation_level, ue_id, cs1_type_str,slot,coreSet0_aggrLvl,cceCnt, 0, 8, cceStart)
    elif test_case_name == "10MHz":
        test_case = TestCase(aggregation_level, ue_id, cs1_type_str,slot,coreSet0_aggrLvl,cceCnt, 8, 16, cceStart)
    elif test_case_name == "15MHz":
        test_case = TestCase(aggregation_level, ue_id, cs1_type_str,slot,coreSet0_aggrLvl,cceCnt, 8, 16, cceStart)
    elif test_case_name == "20MHz":
        test_case = TestCase(aggregation_level, ue_id, cs1_type_str,slot,coreSet0_aggrLvl,cceCnt, 8, 16, cceStart)
    elif test_case_name == "25MHz":
        test_case = TestCase(aggregation_level, ue_id, cs1_type_str,slot,coreSet0_aggrLvl,cceCnt, 16, 16, cceStart)
    elif test_case_name == "100MHz":
        test_case = TestCase(aggregation_level, ue_id, cs1_type_str,slot,coreSet0_aggrLvl,cceCnt, 16, 16, cceStart)
    else:
        print("Invalid test case name")

    create_boxes(test_case)

root = tk.Tk()
root.title("5G PDCCH CCE Allocation")

input_frame = tk.Frame(root)
input_frame.pack(side="top", fill="x", padx=10, pady=10)

# Column 1
label_test_case = tk.Label(input_frame, text="Bandwidth:")
label_test_case.grid(row=0, column=0, sticky="w", padx=5, pady=5)

test_case_var = tk.StringVar()
test_case_menu = ttk.Combobox(input_frame, textvariable=test_case_var)
test_case_menu['values'] = ("5MHz", "10MHz", "15MHz", "20MHz", "25MHz", "100MHz")
test_case_menu.current(1)
test_case_menu.grid(row=0, column=1, padx=5, pady=5)

label_coreSet0_aggrLvl = tk.Label(input_frame, text="CORESET-0 aggregation level:")
label_coreSet0_aggrLvl.grid(row=1, column=0, sticky="w", padx=5, pady=5)

coreSet0_aggrLvl_var = tk.StringVar()
coreSet0_aggrLvl_menu = ttk.Combobox(input_frame, textvariable=coreSet0_aggrLvl_var)
coreSet0_aggrLvl_menu['values'] = ("1", "2", "4", "8")
coreSet0_aggrLvl_menu.current(1)
coreSet0_aggrLvl_menu.grid(row=1, column=1, padx=5, pady=5)

label_aggregation = tk.Label(input_frame, text="CORESET-1 aggregation level:")
label_aggregation.grid(row=2, column=0, sticky="w", padx=5, pady=5)

aggregation_var = tk.StringVar()
aggregation_menu = ttk.Combobox(input_frame, textvariable=aggregation_var)
aggregation_menu['values'] = ("1", "2", "4", "8")
aggregation_menu.current(2)
aggregation_menu.grid(row=2, column=1, padx=5, pady=5)

label_intlvd_cs1 = tk.Label(input_frame, text="Coreset-1 Type:")
label_intlvd_cs1.grid(row=3, column=0, sticky="w", padx=5, pady=5)

cs1_var = tk.StringVar()
cs1_menu = ttk.Combobox(input_frame, textvariable=cs1_var)
cs1_menu['values'] = ("Interleaved", "Non-Interleaved")
cs1_menu.current(1)
cs1_menu.grid(row=3, column=1, padx=5, pady=5)

# Column 2
label_slot = tk.Label(input_frame, text="Slot no:")
label_slot.grid(row=0, column=2, sticky="w", padx=5, pady=5)

slot_var = tk.StringVar()
slot_menu = ttk.Combobox(input_frame, textvariable=slot_var)
slot_menu['values'] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
slot_menu.current(0)
slot_menu.grid(row=0, column=3, padx=5, pady=5)

label_pdcch_symbol = tk.Label(input_frame, text="PDCCH Symbol Count:")
label_pdcch_symbol.grid(row=1, column=2, sticky="w", padx=5, pady=5)

pdcch_symbol_entry = tk.Entry(input_frame)
pdcch_symbol_entry.insert(0, "2")  # Set default value to 2
pdcch_symbol_entry.grid(row=1, column=3, padx=5, pady=5)

label_start_rb = tk.Label(input_frame, text="StartRb:")
label_start_rb.grid(row=2, column=2, sticky="w", padx=5, pady=5)

start_rb_entry = tk.Entry(input_frame)
start_rb_entry.insert(0, "0")  # Set default value to 0
start_rb_entry.grid(row=2, column=3, padx=5, pady=5)

label_ue_id = tk.Label(input_frame, text="Enter UeId (or leave empty for random):")
label_ue_id.grid(row=3, column=2, sticky="w", padx=5, pady=5)

ue_id_entry = tk.Entry(input_frame)
ue_id_entry.grid(row=3, column=3, padx=5, pady=5)

# Button to generate random UeId
random_ue_id_button = tk.Button(input_frame, text="Generate Random UeId", command=lambda: generate_random_ue_id())
random_ue_id_button.grid(row=4, column=3, padx=5, pady=5)

# Execute button
execute_button = tk.Button(
    input_frame,
    text="RUN",
    command=lambda: execute_test_case(
        test_case_var, aggregation_var, ue_id_entry, cs1_var, slot_var, coreSet0_aggrLvl_var,pdcch_symbol_entry, start_rb_entry
    ),
    bg="blue",  # Highlight background color
    fg="white",  # Highlight text color
    font=("Helvetica", 12, "bold")  # Bold font for emphasis
)
execute_button.grid(row=5, column=0, columnspan=4, pady=10)  # Center the button
# Frame to hold canvas and vertical scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Canvas
canvas = tk.Canvas(main_frame, bg="white")
canvas.pack(side="left", fill="both", expand=True)

# Scrollbars
vscrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
vscrollbar.pack(side="right", fill="y")

hscrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
hscrollbar.pack(side="bottom", fill="x")

canvas.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

canvas.config(scrollregion=(0, 0, 6000, 500))

root.mainloop()



