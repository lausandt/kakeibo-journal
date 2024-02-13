import axios from 'axios';

const state = {
  entries: null,
  entry: null
};

const getters = {
  stateEntries: state => state.entries,
  stateEntry: state => state.entry,
};

const actions = {
  async createEntry({dispatch}, entry) {
    await axios.post('entries', entry);
    await dispatch('getEntries');
  },
  async getEntries({commit}) {
    let {data} = await axios.get('entries');
    commit('setEntries', data);
  },
  async viewEntry({commit}, id) {
    let {data} = await axios.get(`entry/${id}`);
    commit('setEntry', data);
  },
  // eslint-disable-next-line no-empty-pattern
  async updateEntry({}, entry) {
    await axios.patch(`entry/${entry.id}`, entry.form);
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteNote({}, id) {
    await axios.delete(`entry/${id}`);
  }
};

const mutations = {
  setNotes(state, notes){
    state.notes = notes;
  },
  setNote(state, note){
    state.note = note;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
}; 