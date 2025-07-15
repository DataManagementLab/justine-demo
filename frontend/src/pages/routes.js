import {createRouter} from 'vue-router'
import Start from "./start/Start.vue";
import Batch from "./batch/Batch.vue";
import Play from "./play/Play.vue";
import Interactive from "./interactive/Interactive.vue";

const routes = [
    {
        name: 'start',
        path: '/',
        component: Start
    },
    {
        name: 'batch',
        path: '/batch/:id/',
        component: Batch
    },
    {
        name: 'play',
        path: '/play/:mode/',
        component: Play
    },
    {
        name: 'interactive_empty',
        path: '/interact/',
        component: Interactive
    },
    {
        name: 'interactive',
        path: '/interact/:id/',
        component: Interactive
    }
]

export default function (history) {
  return createRouter({
    history,
    routes
  })
}
