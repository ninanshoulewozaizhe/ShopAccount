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
            <el-button @click="getSalesDetailfn">查看销量详细统计</el-button>
            <el-button @click="showUpdateDialog = true">更新商品信息</el-button>
            <el-button>更新商品销量</el-button>
            <el-dialog class="p_info_dialog" title="更新信息" :visible.sync="showUpdateDialog">
              <div class="p_info_dialog_container">
                <img class="p_info_img" :src="modifyProduct.img" alt="p_img">
                <el-form>
                  <el-form-item label="商品名称">
                    <el-input class="p_info_name_input" v-model="modifyProduct.name"></el-input>
                  </el-form-item>
                  <el-form-item label="商品描述">
                    <el-input
                      class="p_info_desc_input"
                      type="textarea"
                      :rows="2"
                      placeholder="请输入内容"
                      v-model="modifyProduct.description">
                    </el-input>
                  </el-form-item>
                  <el-form-item label="更新/添加种类库存">
                    <br/>
                    <el-autocomplete
                      class="p_info_new_type_input"
                      v-model="PNewType"
                      :fetch-suggestions="querySearch"
                      placeholder="请输入种类"
                    ></el-autocomplete> : 
                    <el-input class="p_info_new_type_stocks_input" type="number" v-model="PNewTypeAmount"></el-input>
                    <el-button type="primary" @click="updatePType">确定</el-button>
                  </el-form-item>
                </el-form>
                <div>
                  <div class="type_list" v-for="type in Object.keys(modifyProduct.type)" :key="String(type)">
                    <div>{{`${type} : ${modifyProduct.type[type]}`}}</div>
                    <i class="el-icon-delete" @click="deletePType(type)"></i>
                  </div>
                </div>
              </div>
              <div slot="footer" class="dialog-footer">
                <el-button @click="showUpdateDialog = false">取 消</el-button>
                <el-button type="primary" @click="showUpdateDialog = false">确 定</el-button>
              </div>
            </el-dialog>
            <el-dialog class="p_sales_dialog" title="更新销量" :visible.sync="showSalesDialog">
              <div class="p_info_dialog_container">
                <el-form>
                  <el-form-item label="日期选择">
                    <el-date-picker
                      v-model="salesVolumesUpdateDate"
                      type="date"
                      :default-value="new Date()"
                      placeholder="选择日期">
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item label="销量更新">
                      <br/>
                      <el-select>
                        <el-option
                          v-for="item in options"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value"
                          :disabled="item.disable">
                        </el-option>
                      </el-select> : 
                      <el-input class="p_info_new_type_stocks_input" type="number" v-model="PNewTypeAmount"></el-input>
                      <el-button type="primary" @click="updatePType">确定</el-button>
                    </el-form-item>
                </el-form>
                <div>
                  <div class="type_list" v-for="type in Object.keys(modifyProduct.type)" :key="String(type)">
                    <div>{{`${type} : ${modifyProduct.type[type]}`}}</div>
                    <i class="el-icon-delete" @click="deletePType(type)"></i>
                  </div>
                </div>
              </div>
            </el-dialog>
          </div>
          <div class="sales_statistic_btns_g2" v-else>
            <el-button @click="getSalesDetailfn">返回预览</el-button>
            <el-button>利润统计</el-button>
          </div>
        </div>
      </div>
    </div>
    <div class="p_sales_preview" v-if="!getSalesDetail">
      <div class="recent_sales_volumes_statistic">
        <el-radio-group v-model="recentSalesShow">
          <el-radio-button label="stock">商品库存</el-radio-button>
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
    <div class="sales_detail_table" v-else>
      <el-table></el-table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import horizontalSaleTable from '@/components/productDetail/horizontalSaleTable.vue';
import { IProductDetailItem, ISuggestObj } from './typings';

@Component({
  name: 'productDetail',
  components: {
    horizontalSaleTable
  }
})
export default class ProductDetail extends Vue {
  recentSalesShow = 'today';
  getSalesDetail = false;
  showUpdateDialog = false;
  product: IProductDetailItem = {
    id: 1,
    name: '韩版卫衣',
    description: '春秋季新潮品',
    salesVolumes: 11,
    img: AppIcon,
    type: {
      'S': 12,
      'M': 23,
      'L': 12,
      'XL': 23,
      'XXL': 24,
      '3XL': 21,
      '4XL': 23
    }
  };

  modifyProduct: IProductDetailItem = JSON.parse(JSON.stringify(this.product));
  PNewType = '';
  PNewTypeAmount = 0;
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

  getSalesDetailfn() {
    this.getSalesDetail = !this.getSalesDetail;
  }

  querySearch(queryString: string, cb: any) {
    const suggestStrs = this.formatSuggestStrs(Object.keys(this.modifyProduct.type));
    const results = queryString ? suggestStrs.filter(this.createFilter(queryString)) : suggestStrs;
    // 调用 callback 返回建议列表的数据
    cb(results);
  }

  formatSuggestStrs(suggestStrs: string[]): ISuggestObj[] {
    const SuggestStrsObjArr: ISuggestObj[] = [];
    suggestStrs.forEach((str) => {
      SuggestStrsObjArr.push({value: str});
    });
    return SuggestStrsObjArr;
  }

  createFilter(queryString: string) {
    return (type: ISuggestObj) => {
      return (type.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
    };
  }

  deletePType(deleteType: string) {
    const originType = JSON.parse(JSON.stringify(this.modifyProduct.type));
    for (const type in originType) {
      if (type === deleteType) {
        delete originType[type];
        this.$set(this.modifyProduct, 'type', originType);
      }
    }
  }

  updatePType() {
    this.PNewType = this.PNewType.trim();
    if (this.PNewType) {
      this.$set(this.modifyProduct.type, this.PNewType, this.PNewTypeAmount);
    }
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

      .p_info_dialog_container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        
        .p_info_img {
          width: 200px;
          height: 250px;
          margin-bottom: 15px;
        }

        .p_info_name_input, .p_info_desc_input {
          width: 240px;
        }

        .p_info_new_type_input {
          width: 150px;
        }

        .p_info_new_type_stocks_input {
          width: 100px;
          margin-right: 10px;
        }

        .type_list {
          display: flex;
          width: 300px;
          justify-content: space-between;
        }
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
