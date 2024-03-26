const app = Vue.createApp({
    data() {
        return {
            showMenu: false,
            showDropdownMenuConceitos: false,
            showDropdownAccount: false,
            // 
            showConceitosBasicos_01: false,
            showConceitosBasicos_02: false,
            showConceitosBasicos_03: false,
            showConceitosBasicos_04: false,
            showConceitosBasicos_05: false,
            //
            showConceitosInter_01: false,
            showConceitosInter_02: false,
            showConceitosInter_03: false,
            showConceitosInter_04: false,
            //
            showConceitosAvanc_01: false,
            showConceitosAvanc_02: false,
            showConceitosAvanc_03: false,
            showConceitosAvanc_04: false,

        }
    },
    methods: {
        toggleDropdownAccount() {
            this.showDropdownAccount = !this.showDropdownAccount
        },
    }
}
)

app.mount('#app')