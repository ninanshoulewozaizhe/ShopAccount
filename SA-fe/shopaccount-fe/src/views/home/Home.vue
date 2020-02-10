<template>
    <div>
      <product-card :name="'韩版卫衣'" :shop="'好再来服饰'" :salesVolume="11"></product-card>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import productCard from '@/components/home/productCard.vue';

@Component({
  name: 'home',
  components: {
    productCard
  }
})
export default class Home extends Vue {

}
</script>

<style lang="scss" scoped>

</style>