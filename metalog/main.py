import streamlit as st
from tools import instrument_changed, system_changed, add_procedure, get_database
from tools import journal_log, sample_log, instrument_log
import elab
import datetime

def connect2elab():
    endpoint = st.session_state["endpoint"]
    token = st.session_state["token"]
    manager = elab.Manager(endpoint=endpoint, token=token)
    st.session_state.manager = manager
    st.session_state.database = get_database(st.session_state)
    st.session_state.auth = True

def auth():
    with st.form(key='my_form'):
        endpoint = st.text_input(label='Endpoint', key="endpoint")
        token = st.text_input(label='Token', key="token", type="password")
        start = st.form_submit_button(label='Connect', on_click = connect2elab)

def main():
    ## Initialise session state variables
    if "prev_prep" not in st.session_state:
        st.session_state.prev_prep = False
    if "preparation_steps" not in st.session_state:
        st.session_state.preparation_steps = list()

    # Set current date
    now = datetime.datetime.now()
    year = now.strftime("%y")
    st.session_state.year = "20"+year
    month = now.strftime("%m")
    st.session_state.month = month
    day = now.strftime("%d")
    st.session_state.day = day
    st.session_state.date = year + month + day

    database = st.session_state["database"]
    systems_names = ("",) + tuple(database["System"].keys())
    researchers_names = ("",) + tuple(database["Researcher"].keys())
    projects_names = ("",) + tuple(database["Project"].keys())
    topics_names = ("",) + tuple(database["TopicProposal"].keys())
    substrates_names = ("",) + tuple(database["Substrate"].keys())
    procedures_names = ("",) + tuple(database["Procedure"].keys())
    instruments_names = ("",) + tuple(database["Instrument"].keys())

    ### Initialise title and sidebar
    st.set_page_config("MetaLog")

    with st.sidebar:
        st.write("# MetaLog")

    ### Top entries
    system_column, researchers_column = st.columns([1, 3])
    project_column, topic_column = st.columns(2)
    _, journal_column, _ = st.columns(3)

    with system_column:
        system = st.selectbox(
                "System",
                systems_names,
                key = "System",
                help="Select the system in which the Sample Preparation is performed.")
        if system:
            system_changed(st.session_state)

    with researchers_column:
        researcher = st.multiselect(
            "Researcher(s)",
            researchers_names,
            key="Researcher",
            help="Researchers participating in the experiment.")

    with project_column:
        project = st.selectbox(
            "Project",
            projects_names,
            key="Project",
            help="Project related to this experiment.")

    with topic_column:
        topic = st.selectbox(
            "Topic/Proposal",
            topics_names,
            key="TopicProposal",
            help="Topic related to this experiment.")

    with journal_column:
        journal_add = st.button(
            "Create journal",
            key="journal_add",
            on_click=journal_log,
            args=(st.session_state,),
            disabled=st.session_state.prev_prep,
            help="Create a journal entry in the logbook.")

    ### Sample and Instrument columns
    sample_column, instrument_column = st.columns([3, 2])

    ## Sample column
    with sample_column:

        sample_column.subheader("Sample Preparation")

        sample_name = st.text_input(
            "Name",
            key="sample_name",
            disabled=not st.session_state.prev_prep,
            help="Sample ID")

        prev_prep = st.checkbox("Use previous preparation", key="prev_prep")

        sample_substrate = st.selectbox(
            "Substrate",
            substrates_names,
            key="Substrate",
            disabled=st.session_state.prev_prep,
            help="Substrate used for this sample.")

        sample_preparation_id = st.text_input(
            "Preparation ID",
            key="sample_preparation_id",
            disabled=st.session_state.prev_prep,
            help="ID of the preparation (e.g. A1, A2, B1...)")

        procedure = st.selectbox(
            "Select preparation procedure",
            procedures_names,
            key="procedure",
            disabled=st.session_state.prev_prep,
            help="Select a procedure to be added to the Sample Preparation.")

        step_add = st.button(
            "Add step",
            key="step_add",
            disabled=st.session_state.prev_prep,
            help="Add procedure step to the Sample Preparation description.")
        if step_add:
            add_procedure(st.session_state)

        sample_preparation = st.text_area(
            "Sample Preparation description",
            key="sample_preparation",
            disabled=st.session_state.prev_prep,
            help="Full description of Sample Preparation.")

        sample_add = st.button(
            "Conclude and log Sample Preparation",
            key="sample_add",
            on_click=sample_log,
            args=(st.session_state,),
            help="Conclude Sample Preparation and add to logbook.")

    ## Instrument column
    with instrument_column:
        instrument_column.subheader("Instrument")

        instrument = st.selectbox(
            "Instrument",
            instruments_names,
            key = "Instrument",
            help="Select the Instrument to log its parameters.")

        if instrument:
            instrument_changed(st.session_state)

        instrument_add = st.button(
            "Add to log",
            key="instrument_add",
            on_click=instrument_log,
            args=(st.session_state,),
            help="Add Instrument parameters to logbook.")

if "auth" not in st.session_state:
    auth()
else:
    main()
