<template>
  <div>
    <h3>商品详情</h3>
    <div class="p_info_container">
      <img class="p_img" :src="product.img" alt="p_img">
      <div class="p_info">
        <div>
          <div class="p_name">{{ product.name }}</div>
          <div class="p_desc">{{ product.desc }}</div>
        </div>
        <div class="bottom_container">
          <div class="p_sales_volumes">已卖 {{ product.salesVolumes }} 件</div>
          <div class="sales_statistic_btns_g1" v-if="!getSalesDetail">
            <el-button>查看销量详细统计</el-button>
            <el-button>更新销量</el-button>
          </div>
          <div class="sales_statistic_btns_g2" v-else>
            <el-button>返回预览</el-button>
            <el-button>利润统计</el-button>
          </div>
        </div>
      </div>
    </div>
    <div class="recent_sales_volumes_statistic">
      <el-radio-group v-model="recentSalesShow">
        <el-radio-button label="today">今日销量</el-radio-button>
        <el-radio-button label="yesterday">昨日销量</el-radio-button>
      </el-radio-group>
      <horizontalSaleTable class="sales_table" :data="productSales"></horizontalSaleTable>
    </div>
    <div class="products_sales_date">
      <h3>销量统计</h3>
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
      <ve-line></ve-line>
    </div>
    <div class="product_sales_prediect">
      <h3>销量预测（未来一周）</h3>
      <ve-line></ve-line>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import horizontalSaleTable from '@/components/productDetail/horizontalSaleTable.vue';

@Component({
  name: 'productDetail',
  components: {
    horizontalSaleTable
  }
})
export default class ProductDetail extends Vue {
  recentSalesShow = 'today';
  getSalesDetail = false;
  product = {
    name: '韩版卫衣',
    desc: '春秋季新潮品',
    salesVolumes: 11,
    img: AppIcon
  };

  productSales = {
    'S': 12,
    'M': 23,
    'L': 12,
    'XL': 23,
    'XXL': 24,
    '3XL': 21,
    '4XL': 23
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

  datePickerChange() {
    console.log(this.salesDatePick);
  }
}
</script>

<style lang="scss" scoped>
.p_info_container {
  display: flex;
  .p_img {
    width: 200px;
    height: 250px;
    margin: 0 20px 20px 20px;
  }

  .p_info {
    position: relative;
    height: 250px;

    .p_name, .p_desc {
      font-size: 18px;  
    }

    .p_name {
      font-weight: bold;
      margin-bottom: 10px;
    }

    .bottom_container {
      position: absolute;
      bottom: 0;

      .p_sales_volumes {
        font-weight: bold;
        margin-bottom: 10px;
      }
      .sales_statistic_btns_g1, .sales_statistic_btns_g2 {
        display: flex;
      }
    }
  }
}

.recent_sales_volumes_statistic {
  margin-top: 20px;

  .sales_table {
    margin-top: 10px;
  }
}
</style>