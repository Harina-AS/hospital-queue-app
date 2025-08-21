import streamlit as st
import heapq
from collections import deque

# ---------------- Hospital Queue Logic ----------------
class HospitalQueue:
    def __init__(self):
        self.normal_queue = deque()
        self.emergency_queue = []

    def add_patient(self, name, priority=0):
        if priority == 0:
            self.normal_queue.append(name)
            return f"Added NORMAL patient: {name}"
        else:
            heapq.heappush(self.emergency_queue, (-priority, name))
            return f"Added EMERGENCY patient: {name} (priority {priority})"

    def treat_patient(self):
        if self.emergency_queue:
            priority, name = heapq.heappop(self.emergency_queue)
            return f"Treating EMERGENCY patient: {name} (priority {-priority})"
        elif self.normal_queue:
            name = self.normal_queue.popleft()
            return f"Treating NORMAL patient: {name}"
        else:
            return "No patients waiting."

    def show_waiting_list(self):
        result = []
        if self.emergency_queue:
            result.append("Emergency Patients:")
            for p, name in sorted(self.emergency_queue, reverse=True):
                result.append(f"  {name} (priority {-p})")
        else:
            result.append("No emergency patients.")

        if self.normal_queue:
            result.append("Normal Patients:")
            for name in self.normal_queue:
                result.append(f"  {name}")
        else:
            result.append("No normal patients.")

        return "\n".join(result)


# ---------------- Streamlit App ----------------
hospital = HospitalQueue()

st.title("🏥 Hospital Patient Queue System")

menu = ["Add Patient", "Treat Next Patient", "Show Waiting List"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Patient":
    st.subheader("➕ Add Patient")
    name = st.text_input("Enter Patient Name")
    priority = st.number_input("Enter Priority (0 = Normal, >0 = Emergency)", min_value=0, step=1)
    if st.button("Add"):
        if name.strip():
            result = hospital.add_patient(name, priority)
            st.success(result)
        else:
            st.warning("Please enter a patient name.")

elif choice == "Treat Next Patient":
    st.subheader("🩺 Treat Next Patient")
    if st.button("Treat"):
        result = hospital.treat_patient()
        st.info(result)

elif choice == "Show Waiting List":
    st.subheader("📋 Waiting List")
    result = hospital.show_waiting_list()
    st.text(result)
