import Vue from "vue";
import Buefy from "buefy";
import Home from "./components/Home";
import TrophyDistribution from "./components/TrophyDistribution";
import bugsnag from "./bugsnag";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#app",
  components: {
    Home,
    TrophyDistribution
  }
});
