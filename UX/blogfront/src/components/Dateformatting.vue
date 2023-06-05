<template>
    <div id="app">
        <p>{{ dateonly }} {{ year }}, {{ hourcomputed }}:{{ minsonly }}{{ timeofday }}</p>
    </div>
</template>
 
<script>

export default {
    name: "Dateformatting",
    props:['create_date'],
    data() {
        return{
            "full_date":new Date(Date.parse(this.create_date)).toString(),
            "dateonly":new Date(Date.parse(this.create_date)).toString().substring(4, 10),
            "year":new Date(Date.parse(this.create_date)).toString().substring(11, 15),
            "timeonly":new Date(Date.parse(this.create_date)).toString().substring(16, 21),
            "hour" : parseInt(new Date(Date.parse(this.create_date)).toString().substring(16, 18)),
            "minsonly":new Date(Date.parse(this.create_date)).toString().substring(19, 21),
             
            

        }
    },
    computed:{
        timeofday() {
            return this.hour >12 ? "pm": "am"
        },
        hourcomputed() {
            return this.hour > 12 ? this.hour-12 : this.hour
        },
    }
    }
</script>