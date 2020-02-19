<template>
  <div>
    <div class="table">
      <div class="table_row talbe_row_1">
        <div class="table_head">种类</div>
        <div class="table_cell" v-for="(item, index) in data" :key="index">{{ item.type }}</div>
        <div class="table_cell">总计</div>
      </div>
      <div class="table_row table_row_2">
        <div class="table_head">数量</div>
        <div class="table_cell" v-for="(item, index) in data" :key="index">{{ item.amount }}</div>
        <div class="table_cell">{{ salesSum }}</div>
      </div>
      </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import { IndexOJ } from './typings';
import { IProductSalesItem } from '@/views/productDetail/typings';


@Component({
  name: 'horizontalSaleTable'
})
export default class HorizontalSaleTable extends Vue {

@Prop() readonly data!: IProductSalesItem[];

  get salesSum() {
    return this.data.reduce((pre, cur) => {
      return pre + cur.amount;
    }, 0);
  }
}
</script>

<style lang="scss" scoped>
.table_row {
  display: flex;
  text-align: center;
  line-height: 30px;
  .table_head {
    border: 1px solid grey;
    width: 100px;
    height: 30px;
  }
  .table_cell {
    border: 1px solid grey;
    border-left: 0px;
    width: 100px;
    height: 30px;
  }
}

.table_row_2 {
  .table_head, .table_cell {
    border-top: 0px;
  }
}
</style>