import streamlit as st
import sys
import elab

def journal_log(state):

    if not state.System:
        st.warning("Select at least a System before creating a journal entry.")
        state.journal_exp = None
    else:
        title = state.year+"-"+state.month+"-"+state.day
        journal_exp = state.manager.create_experiment()
        journal_exp.update(
            title=title,
            date="20"+state.date,
            body="",
            links=get_links(state, ["Project", "TopicProposal", "Researcher"]),
            )
        status_id = get_status_id(state)
        if status_id:
            journal_exp.update(category=status_id)
        st.success("Journal entry {0} created.".format(title))
        state.journal_exp = journal_exp

def sample_log(state):

    if "journal_exp" not in state:
        st.warning("Create a journal entry before logging a Sample Preparation.")
        state.sample_exp = None
        return
    elif not state.prev_prep and not all([state.sample_name, state.sample_preparation_id, state.sample_preparation]):
        st.warning("Provide at least Name, Preparation ID and Description.")
        state.sample_exp = None
        return
    elif state.prev_prep and not state.sample_name:
        st.warning("Provide at least Sample Preparation Name.")
        state.sample_exp = None
        return
    else:
        title = state.sample_name+state.sample_preparation_id
        if not state.prev_prep:
            sample_exp = state.manager.create_experiment()
            sample_exp.update(
                title=title,
                date="20"+state.date,
                body=state.sample_preparation,
                links=get_links(state, ["Substrate"]),
                tags=[title]
                )
            status_id = get_status_id(state, is_sample=True)
            if status_id:
                sample_exp.update(category=status_id)
            state.sample_exp = sample_exp

        state.journal_exp.update(
            #links=[state.sample_exp.expid],
            tags=[title]
            )
        st.success("Sample entry {0} logged.".format(title))

def instrument_log(state):
    pass

def get_links(state, categories):
    links = list()
    for cat in categories:
        if state[cat]:
            if type(state[cat]) is list:
                for e in state[cat]:
                    links.append(state.database[cat][e])
            else:
                links.append(state.database[cat][state[cat]])
    return links

def get_status_id(state, is_sample=False):
    if is_sample:
        category = "Sample"
    else:
        category = state.System
    status_id = None
    all_status = state.manager.get_all_status()
    for status in all_status:
        if status["category"] == category:
            status_id = status["category_id"]
    return status_id

def instrument_changed(state):
    pass

def system_changed(state):

    date = state.date

    if not state.prev_prep:
        if state.System == "":
            state.sample_name = ""
        else:
            state.sample_name = state.System[0:2] + date

def add_procedure(state):
    procedure = state.procedure
    procedures = state.database["ProcedureMeta"]
    if procedure != "":
        state.sample_preparation += procedures[procedure]

def get_database(state):

    items = state.manager.get_all_items(params={'limit': 9999, 'offset': 0})
    types = state.manager.get_items_types()
    database = dict()

    for t in types:
        database[t["category"]] = dict()

    for item in items:
        database[item["category"]][item["title"]] = item["id"]

    # Merge Topic and Proposals
    database["TopicProposal"] = dict(database["Topic"])
    database["TopicProposal"].update(database["Proposal"])

    # Create Procedures field
    database["ProcedureMeta"] = dict()
    for k, v in database["Procedure"].items():
        item = state.manager.get_item(v)
        meta = item["body"]
        database["ProcedureMeta"][k] = meta

    return database
