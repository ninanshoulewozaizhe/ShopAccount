<template>
  <div>
    <h3>店铺管理</h3>
    <div class="s_info_container">
      <img class="s_img" :src="shop.img" alt="s_img">
      <div class="s_info">
        <div>
          <div class="s_name">{{ shop.name }}</div>
          <div class="s_desc">{{ shop.description }}</div>
        </div>
        <div class="bottom_container">
          <div class="s_sales_volumes">已卖 {{ shop.salesVolume }} 件</div>
          <div class="sales_statistic_btns_g1" v-if="!getSalesDetail">
            <el-button @click="getSalesDetailfn">查看销量详细统计</el-button>
            <el-button @click="updateShopDialog = true">更新店铺信息</el-button>
            <el-button @click="AddNewProductDialog = true">添加商品</el-button>
            <el-button type="danger">删除店铺</el-button>
            <el-dialog class="p_info_dialog" title="更新店铺信息" :visible.sync="updateShopDialog">
              <div class="p_info_dialog_container">
                <img class="p_info_img" :src="modifyShop.img" alt="p_img">
                <el-form>
                  <el-form-item label="店铺名称">
                    <el-input class="p_info_name_input"
                    v-model="modifyShop.name"
                    placeholder="请输入名称"></el-input>
                  </el-form-item>
                  <el-form-item label="店铺描述">
                    <el-input
                      class="p_info_desc_input"
                      type="textarea"
                      :rows="2"
                      placeholder="请输入内容"
                      v-model="modifyShop.description">
                    </el-input>
                  </el-form-item>
                </el-form>
              </div>
              <div slot="footer" class="dialog-footer">
                <el-button @click="updateShopDialog = false">取 消</el-button>
                <el-button type="primary" @click="updateShopDialog = false">确 定</el-button>
              </div>
            </el-dialog>
            <el-dialog class="p_info_dialog" title="添加商品" :visible.sync="AddNewProductDialog">
              <div class="p_info_dialog_container">
                <img class="p_info_img" :src="newProduct.img" alt="p_img">
                <el-form>
                  <el-form-item label="商品名称">
                    <el-input class="p_info_name_input"
                    v-model="newProduct.name"
                    placeholder="请输入名称"></el-input>
                  </el-form-item>
                  <el-form-item label="商品描述">
                    <el-input
                      class="p_info_desc_input"
                      type="textarea"
                      :rows="2"
                      placeholder="请输入内容"
                      v-model="newProduct.description">
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
                  <div class="type_list" v-for="type in Object.keys(newProduct.type)" :key="String(type)">
                    <div>{{`${type} : ${newProduct.type[type]}`}}</div>
                    <i class="el-icon-delete" @click="deletePType(type)"></i>
                  </div>
                </div>
              </div>
              <div slot="footer" class="dialog-footer">
                <el-button @click="AddNewProductDialog = false">取 消</el-button>
                <el-button type="primary" @click="AddNewProductDialog = false">确 定</el-button>
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
    <div class="s_sales_preview" v-if="!getSalesDetail">
      <div class="product_list">
        <h3>商品列表</h3>
        <product-list 
        :allProducts="allProducts"
        :showPageSize="showPageSize"
        ></template>
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
    </div>
    <div class="sales_detail_table" v-else>
      <el-table></el-table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import productList from '@/components/home/productList.vue';
import { IProductDetailItem, ISuggestObj, IProductSalesItem } from '@/typing/productDetail/typings';
import { IShopItem } from '@/typing/shops/typings';
import { IProductItem } from '@/typing/home/typings';

@Component({
  name: 'shopManage',
  components: {
    productList
  }
})
export default class ShopManage extends Vue {
  getSalesDetail = false;
  updateShopDialog = false;
  AddNewProductDialog = false;
  showSalesDialog = false;
  shop: IShopItem = {
    id: 1,
    name: '好再来服饰',
    description: '春秋季新潮品',
    salesVolume: 11,
    productAmount: 11,
    img: AppIcon
  };

  modifyShop: IShopItem = JSON.parse(JSON.stringify(this.shop));

  newProduct: IProductDetailItem = {
    id: -1,
    name: '',
    description: '',
    salesVolumes: 0,
    img: AppIcon,
    type: {}
  };
  PNewType = '';
  PNewTypeAmount = 0;
  allProducts: IProductItem[] = [
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
  showPageSize = 8;

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
    const suggestStrs = this.formatSuggestStrs(Object.keys(this.newProduct.type));
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
    const originType = JSON.parse(JSON.stringify(this.newProduct.type));
    for (const type in originType) {
      if (type === deleteType) {
        delete originType[type];
        this.$set(this.newProduct, 'type', originType);
      }
    }
  }

  updatePType() {
    this.PNewType = this.PNewType.trim();
    if (this.PNewType) {
      this.$set(this.newProduct.type, this.PNewType, this.PNewTypeAmount);
    }
  }

}
</script>

<style lang="scss" scoped>
.s_info_container {
  display: flex;
  .s_img {
    width: 200px;
    height: 250px;
    margin: 0 20px 20px 20px;
  }

  .s_info {
    position: relative;
    height: 250px;

    .s_name, .s_desc {
      font-size: 18px;  
    }

    .s_name {
      font-weight: bold;
      margin-bottom: 10px;
    }

    .bottom_container {
      position: absolute;
      bottom: 0;

      .s_sales_volumes {
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
