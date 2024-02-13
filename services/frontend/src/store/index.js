import { createStore } from "vuex";

import users from "./modules/users"
import entries from "./modules/entries"

export default createStore({
    modules: {
        entries, 
        users,
    }
});