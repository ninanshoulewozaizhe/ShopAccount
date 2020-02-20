<template>
  <div>
    <div class="products_preview">
      <div>
        <h3>店内商品</h3>
      </div>
      <div class="products_container">
        <div class="card_wrapper" v-for="product in showProducts" 
          :key="product.id" @click="getProductDetail(product.id)">
          <product-card class="p_card"  
          :name="product.name" 
          :salesVolume="product.salesVolume"></product-card>
        </div>
        <span class="product_get_more" @click="getShopManage">店铺管理>></span>
    </div>
    </div>
    <div class="shop_sales_statistics">
      <div class="products_sales_today">
        <h3>今日商品销量(总计: {{ productSalesVolumeToday }} 件)</h3>
        <el-table class="sales_show_table" :data="showTable" border>
          <el-table-column align="center" prop="name" label="商品名称" width="300"></el-table-column>
          <el-table-column align="center" prop="salesVolume" label="销量" ></el-table-column>
        </el-table>
        <el-pagination class="table_pagination" layout="prev, pager, next" 
        :total="allTableData.length"
        :page-size="showtableSize"
        @current-change="tablePageChange"></el-pagination>
      </div>
      <div class="products_sales_date">
        <h3>店铺销量统计</h3>
        <span>日期选择：</span>
        <el-date-picker
          v-model="salesDatePick"
          type="daterange"
          align="right"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :picker-options="datePickerOptions"
          @change="datePickerChange">
        </el-date-picker>
        <ve-line :data="chartData"></ve-line>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import { IProductItem } from '@/typing/home/typings';
import productCard from '@/components/home/productCard.vue';

@Component({
  name: 'shopDetail',
  components: {
    productCard
  }
})
export default class ShopDetail extends Vue {
  allTableData: IProductItem[] = [
    {id: 1, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 2, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 3, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 4, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 5, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 6, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 7, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 8, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 9, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 10, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 11, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 12, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 13, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 14, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'}
    ];
  showtableSize = 4;
  showTable: IProductItem[]  = [];
  showProducts: IProductItem[] = [
    {id: 1, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 13, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 2, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 3, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'}
    ];

  chartData = {
    columns: ['日期', '销量'],
    rows: [
      { 日期: '1/1', 销量: 1393},
      { 日期: '1/2', 销量: 3530},
      { 日期: '1/3', 销量: 2923},
      { 日期: '1/4', 销量: 1723},
      { 日期: '1/5', 销量: 3792},
      { 日期: '1/5', 销量: 3792},
      { 日期: '1/5', 销量: 3792},
      { 日期: '1/5', 销量: 3792},
      { 日期: '1/6', 销量: 4593}
    ]
  };


  datePickerOptions = {
    shortcuts: [{
      text: '最近一周',
      onClick(picker: any) {
        const end = new Date();
        const start = new Date();
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
        picker.$emit('pick', [start, end]);
      }
    }, {
      text: '最近一个月',
      onClick(picker: any) {
        const end = new Date();
        const start = new Date();
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
        picker.$emit('pick', [start, end]);
      }
    }],
    disabledDate(curDate: any) {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 31);
      return curDate < start || curDate > end;
    }
  };

  salesDatePick = [];

  mounted() {
    this.showTableInit();
  }

  showTableInit() {
    for (let i = 0; i < this.showtableSize && i < this.allTableData.length; ++i) {
      this.showTable.push(this.allTableData[i]);
    }
  }

  get productSalesVolumeToday() {
    return this.allTableData.reduce((pre, cur) => {
      return pre + cur.salesVolume;
    }, 0);
  }

  tablePageChange(curPage: number) {
    this.showTable = [];
    for (let i = this.showtableSize * (curPage - 1), time = 0;
    time < this.showtableSize && i < this.allTableData.length; ++i, ++time) {
      this.showTable.push(this.allTableData[i]);
    }
  }

  datePickerChange() {
    console.log(this.salesDatePick);
  }

  getProductDetail(pid: number) {
    this.$router.push({
      name: 'product-detail',
      params: {
        pid: String(pid)
      }
    });
  }

  getShopManage() {
    const sid = this.$route.params.sid;
    this.$router.push({
      name: 'shop-manage',
      params: {
        sid: String(sid)
      }
    });
  }
}
</script>

<style lang="scss" scoped>
.products_preview {
  .card_wrapper {
    display: inline-block;

    .p_card {
      margin-right: 20px;
    }
  }
  

  .product_get_more {
    position: relative;
    bottom: 3px;
  }

  .product_get_more:hover {
    font-weight: bold;
    cursor: pointer;
    
  }
}

.shop_sales_statistics {

  .products_sales_today {
    width: 40%;
  }

  .table_pagination {
    float: right;
    margin-top: 10px;
  }

  .products_sales_date {
    margin-top: 60px;

    span {
      font-weight: bold;
    }
  }
}
</style>