<template>
  <div>
    <h3>商品详情</h3>
    <div class="p_info_container">
      <img class="p_img" v-if="product.img" :src="`/getImg?f=${product.img}`" alt="p_img">
      <div class="p_info">
        <div>
          <div class="p_name">{{ product.name }}</div>
          <div class="p_desc">{{ product.description }}</div>
        </div>
        <div class="bottom_container">
          <div class="p_sales_volumes">已卖 {{ product.salesVolumes }} 件</div>
          <div class="sales_statistic_btns_g1" v-if="!getSalesDetail">
            <el-button @click="getSalesDetailfn">查看销量详细统计</el-button>
            <el-button @click="showUpdateDialog = true">更新商品信息</el-button>
            <el-button @click="showSalesDialog = true">更新商品销量</el-button>
            <el-dialog class="p_info_dialog" title="更新信息" :visible.sync="showUpdateDialog">
              <div class="p_info_dialog_container">
                <el-upload
                  class="img-uploader"
                  action="/shopImg"
                  :show-file-list="false"
                  :on-success="imgUploadSuccess"
                  :before-upload="beforeImgUpload">
                  <img v-if="modifyProduct.img" :src="`/getImg?f=${modifyProduct.img}`" class="p_info_img">
                  <i v-else class="el-icon-plus img-uploader-icon"></i>
                </el-upload>
                <el-form>
                  <el-form-item label="商品名称">
                    <el-input class="p_info_name_input"
                    v-model="modifyProduct.name"
                    placeholder="请输入名称"></el-input>
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
                <el-button @click="cancelProductUpdate">取 消</el-button>
                <el-button type="primary" @click="submitProductUpdate">确 定</el-button>
              </div>
            </el-dialog>
            <el-dialog class="p_sales_dialog" title="更新销量" :visible.sync="showSalesDialog">
              <div class="p_info_dialog_container">
                <el-form>
                  <el-form-item label="日期选择">
                    <el-date-picker
                      v-model="salesVolumesUpdateDate"
                      type="date"
                      @change="updateSalesdatePickerChange"
                      placeholder="选择日期">
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item label="销量更新">
                      <br/>
                      <el-select v-model="PSalesUpadteType">
                        <el-option
                          v-for="item in Object.keys(updateSales)"
                          :key="item"
                          :label="item"
                          :value="item"
                        >
                        </el-option>
                      </el-select> : 
                      <el-input class="p_info_new_type_stocks_input" type="number" v-model="PSalesUpadteAmount"></el-input>
                      <el-button type="primary" @click="updatePSales">确定</el-button>
                    </el-form-item>
                </el-form>
                <div>
                  <div class="type_list" v-for="(value, name) in updateSales" :key="name">
                    <div>{{`${name} : ${value}`}}</div>
                  </div>
                </div>
                <div slot="footer" class="dialog-footer update_sales_footer">
                <el-button @click="cancelUpdateSales">取 消</el-button>
                <el-button type="primary" @click="submitUpdateSales">确 定</el-button>
              </div>
              </div>
            </el-dialog>
          </div>
          <div class="sales_statistic_btns_g2" v-else>
            <el-button @click="getSalesDetailfn">返回预览</el-button>
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
        <horizontalSaleTable class="sales_table" :data="HtableDatashow"></horizontalSaleTable>
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
          :clearable="false"
          :picker-options="datePickerOptions"
          @change="datePickerChange">
        </el-date-picker>
          <ve-line :data="chartData"></ve-line>
      </div>
    </div>
    <div class="sales_detail_table" v-else>
      <h3>销量详细统计</h3>
      <span>日期选择：</span>
        <el-date-picker
          v-model="salesDatePick"
          type="daterange"
          align="right"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :clearable="false"
          :picker-options="datePickerOptions"
          @change="datePickerChange">
        </el-date-picker>
        <div class="table_container">
          <el-table 
            border
            :data="salesDetailTableData">
            <el-table-column
              prop="date"
              label="日期"
              sortable
              fixed
              align="center"
              width="180">
            </el-table-column>
            <el-table-column v-for="item in Object.keys(product.type)" :key="item"
            :prop="item"
            :label="item"
            align="center"
            sortable
            width="120">
            </el-table-column>
            <el-table-column
              prop="salesVolumes"
              label="总计"
              sortable
              fixed="right"
              align="center"
              width="150">
            </el-table-column>
          </el-table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import horizontalSaleTable from '@/components/productDetail/horizontalSaleTable.vue';
import { IProductDetailItem, ISuggestObj, IProductSalesItem,
  IndexStingOJ, IndexOJ, SalesChartRowItem, SalesChartData } from '@/typing/productDetail/typings';
import store from '@/store';
import { LOAD_CUR_PRODUCT, GET_CUR_PRODUCT, UPDATE_PRODUCT } from '@/store/modules/product/constants';
import { LOAD_CUR_PRODUCT_TODAY_SALES, LOAD_CUR_PRODUCT_YESTERDAY_SALES,
  GET_CUR_PRODUCT_TODAY_SALES, GET_CUR_PRODUCT_YESTERDAY_SALES,
  GET_PRODUCT_ONE_DAY_SALES, MODIFY_PRODUCT_ONE_DAY_SALES,
  LOAD_PRODUCT_ONE_DAY_SALES, UPDATE_PRODUCT_ONE_DAY_SALES,
  LOAD_PRODUCT_PERIOD_SALES, GET_PRODUCT_PERIOD_SALES
  } from '@/store/modules/salesStatus/constants';
import { SalesRecordItem } from '@/typing/salesStatus/typings';

@Component({
  name: 'productDetail',
  components: {
    horizontalSaleTable
  },
  async beforeRouteEnter(to: any, from: any, next: any) {
    const pid = to.params.pid;
    const todayStr = new Date().toISOString().split('T')[0];
    const yesterdayStr = new Date(+new Date() - 1000 * 60 * 60 * 24).toISOString().split('T')[0];
    const weekAgoStr = new Date(+new Date() - 3600 * 1000 * 24 * 6).toISOString().split('T')[0];
    console.log(todayStr);
    console.log(weekAgoStr);
    await store.dispatch(`product/${LOAD_CUR_PRODUCT}`, pid);
    await store.dispatch(`salesStatus/${LOAD_CUR_PRODUCT_TODAY_SALES}`, {pid, date: todayStr});
    await store.dispatch(`salesStatus/${LOAD_CUR_PRODUCT_YESTERDAY_SALES}`, {pid, date: yesterdayStr});
    await store.dispatch(`salesStatus/${LOAD_PRODUCT_PERIOD_SALES}`, {pid, from: weekAgoStr, to: todayStr});
    const product = store.getters[`product/${GET_CUR_PRODUCT}`];
    const todaySales = store.getters[`salesStatus/${GET_CUR_PRODUCT_TODAY_SALES}`];
    const yesterdaySales = store.getters[`salesStatus/${GET_CUR_PRODUCT_YESTERDAY_SALES}`];
    const chartRowRawData = store.getters[`salesStatus/${GET_PRODUCT_PERIOD_SALES}`];
    console.log(chartRowRawData);
    next((vm: any) => {
      vm.product = JSON.parse(JSON.stringify(product));
      vm.modifyProduct = JSON.parse(JSON.stringify(product));
      vm.chartDataInit(chartRowRawData, new Date(+new Date() - 3600 * 1000 * 24 * 6), new Date());
      vm.salesInit(vm.todaySales, todaySales);
      vm.salesInit(vm.yesterdaySales, yesterdaySales);
      vm.salesInit(vm.updateSales, todaySales);
      vm.salesDetailTableDataInit(chartRowRawData, new Date(+new Date() - 3600 * 1000 * 24 * 6), new Date());
    });
  }
})
export default class ProductDetail extends Vue {
  recentSalesShow = 'today';
  getSalesDetail = false;
  showUpdateDialog = false;
  showSalesDialog = false;
  salesVolumesUpdateDate = new Date();
  updateDatePickerUse = false;
  product: IProductDetailItem = {
    id: -1,
    name: '',
    description: '',
    salesVolumes: 0,
    img: '',
    sid: -1,
    shop: '',
    type: {}
  };

 SalesDetailData: SalesRecordItem[] = [];

  chartData: SalesChartData = {
    columns: ['日期', '销量'],
    rows: []
  };

  salesDetailTableData: any = [];

  modifyProduct: IProductDetailItem = JSON.parse(JSON.stringify(this.product));
  PNewType = '';
  PNewTypeAmount = 0;
  PSalesUpadteType = '';
  PSalesUpadteAmount = 0;

  datePickerOptions = {
    shortcuts: [{
      text: '最近一周',
      onClick(picker: any) {
        const end = new Date();
        const start = new Date();
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 6);
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

  salesDatePick = [new Date(+new Date() - 3600 * 1000 * 24 * 6), new Date()];

  todaySales: IndexStingOJ = {};
  yesterdaySales: IndexStingOJ = {};
  updateSales: IndexStingOJ = {};

  salesInit(obj: any, data: SalesRecordItem | null) {
    if (data && data.sales) {
      if (typeof data.sales === 'string') {
        const sales = JSON.parse(data.sales);
        for (const type in sales) {
          if (type) {
            this.$set(obj, type, sales[type]);
          }
        }
      }
    } else {
      for (const type in this.product.type) {
        if (type) {
          this.$set(obj, type, 0);
        }
      }
    }
  }

  salesDetailTableDataInit(salesRecords: SalesRecordItem[], from: Date, to: Date) {
    this.salesDetailTableData = [];
    let temp = from;
    let tempDateStr = temp.toISOString().split('T')[0];
    const endDateStr = to.toISOString().split('T')[0];
    for (const item of salesRecords) {
      const rDate = new Date(item.date).toISOString().split('T')[0];
      while (rDate !== tempDateStr) {
        const data = {
          date: tempDateStr,
          salesVolumes: 0
        };
        for (const type in this.product.type) {
          if (type) {
            this.$set(data, type, 0);
          }
        }
        this.salesDetailTableData.push(data);
        temp = new Date(+temp + 3600 * 1000 * 24);
        tempDateStr = temp.toISOString().split('T')[0];
      }
      if (typeof item.sales === 'string') {
        const data = JSON.parse(item.sales);
        const sales = JSON.parse(item.sales);
        data.date = rDate;
        data.salesVolumes = Object.values(sales).reduce((pre: number, cur: number) => {
          return pre + (+cur);
        }, 0);
        this.salesDetailTableData.push(data);
        temp = new Date(+temp + 3600 * 1000 * 24);
        tempDateStr = temp.toISOString().split('T')[0];
      }
    }
    while (tempDateStr <= endDateStr) {
      const data = {
        date: tempDateStr,
        salesVolumes: 0
      };
      for (const type in this.product.type) {
        if (type) {
          this.$set(data, type, 0);
        }
      }
      this.salesDetailTableData.push(data);
      temp = new Date(+temp + 3600 * 1000 * 24);
      tempDateStr = temp.toISOString().split('T')[0];
    }
    console.log(this.salesDetailTableData);
  }

  chartDataInit(rowRawData: SalesRecordItem[], from: Date, to: Date) {
    const datePeriodObj: SalesChartRowItem[] = this.datePeriodObjInit(from, to);
    for (const record of rowRawData) {
      if (record) {
        for (const rowItem of datePeriodObj) {
          const rdate = new Date(record.date).toISOString().split('T')[0];
          if (rowItem.日期 === rdate) {
            if (typeof record.sales === 'string') {
              const data: IndexOJ = JSON.parse(record.sales);
              rowItem.销量 += Object.values(data).reduce((pre: number, cur: number) => {
                return pre + (+cur);
              }, 0);
            }
          }
        }
      }
    }
    this.$set(this.chartData, 'rows', datePeriodObj);
    console.log(this.chartData);
  }

  datePeriodObjInit(from: Date, to: Date): SalesChartRowItem[] {
    const datePeriodObj: SalesChartRowItem[] = [];
    let temp = from;
    const endDateStr = to.toISOString().split('T')[0];
    for (let i = 1; temp.toISOString().split('T')[0] <= endDateStr; ++i) {
      const tempRowItem: SalesChartRowItem = {
        日期: temp.toISOString().split('T')[0],
        销量: 0
      };
      datePeriodObj.push(tempRowItem);
      temp = new Date(+from + 3600 * 1000 * 24 * i);
    }
    return datePeriodObj;
  }

  get HtableDatashow() {
    const data: IndexStingOJ = {
      stock: this.product.type || {},
      today: this.todaySales  || {},
      yesterday: this.yesterdaySales || {}
    };
    return data[this.recentSalesShow];
  }

  async datePickerChange() {
    console.log(this.salesDatePick);
    const fixDatePick = [new Date(+this.salesDatePick[0] + 3600 * 1000 * 24),
      new Date(+this.salesDatePick[1] + 3600 * 1000 * 24)];
    const from = fixDatePick[0].toISOString().split('T')[0];
    const to = fixDatePick[1].toISOString().split('T')[0];
    await this.$store.dispatch(`salesStatus/${LOAD_PRODUCT_PERIOD_SALES}`, {pid: this.product.id, from, to});
    const data = store.getters[`salesStatus/${GET_PRODUCT_PERIOD_SALES}`];
    this.salesDetailTableDataInit(data, fixDatePick[0], fixDatePick[1]);
    this.chartDataInit(data, fixDatePick[0], fixDatePick[1]);
  }

  async updateSalesdatePickerChange() {
    this.updateDatePickerUse = true;
    const updateDate = new Date(+this.salesVolumesUpdateDate + 1000 * 60 * 60 * 24).toISOString().split('T')[0];
    console.log(updateDate);
    await this.$store.dispatch(`salesStatus/${LOAD_PRODUCT_ONE_DAY_SALES}`, {pid: this.product.id, date: updateDate});
    const record = this.$store.getters[`salesStatus/${GET_PRODUCT_ONE_DAY_SALES}`];
    console.log('new record:', record);
    if (record && record.sales) {
      // const sales = JSON.parse(record.sales);
      // this.updateSales = {};
      // for (const type in sales) {
      //   if (type) {
      //     this.$set(this.updateSales, type, sales[type]);
      //   }
      // }
      this.updateSales = JSON.parse(record.sales);
    } else {
      for (const type in this.product.type) {
        if (type) {
          this.$set(this.updateSales, type, 0);
        }
      }
    }
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

  updatePSales() {
    console.log(this.updateSales);
    console.log(this.PSalesUpadteType);
    this.$set(this.updateSales, this.PSalesUpadteType, +this.PSalesUpadteAmount);
  }

  updateSalesDataInit() {
    this.PSalesUpadteType = '';
    this.PSalesUpadteAmount  = 0;
    this.updateSales = JSON.parse(JSON.stringify(this.todaySales));
    this.salesVolumesUpdateDate = new Date();
  }

  cancelUpdateSales() {
    this.updateSalesDataInit();
    this.showSalesDialog = false;
    this.updateDatePickerUse = false;
  }

  async submitUpdateSales() {
    let updateDate;
    if (this.updateDatePickerUse) {
      updateDate = new Date(+this.salesVolumesUpdateDate + 1000 * 60 * 60 * 24).toISOString().split('T')[0];
    } else {
      updateDate = this.salesVolumesUpdateDate.toISOString().split('T')[0];
    }
    console.log(updateDate);
    const fileds = Object.freeze({
      pid: this.product.id,
      date: updateDate,
      sid: this.product.sid,
      pname: this.product.name,
      sales: JSON.stringify(this.updateSales)});
    const result = await this.$store.dispatch(`salesStatus/${UPDATE_PRODUCT_ONE_DAY_SALES}`, fileds);
    await store.dispatch(`product/${LOAD_CUR_PRODUCT}`, this.product.id);
    const productnewInfo = this.$store.getters[`product/${GET_CUR_PRODUCT}`];
    this.product = JSON.parse(JSON.stringify(productnewInfo));
    this.modifyProduct = JSON.parse(JSON.stringify(productnewInfo));
    if (result === 'OK') {
      this.$notify({
        title: '更新成功',
        message: '销量更新成功',
        type: 'success'
      });
    } else {
      this.$notify.error({
        title: '更新失败',
        message: '销量更新失败，请稍后再试'
      });
    }
    const today = new Date().toISOString().split('T')[0];
    if (updateDate === today) {
      this.todaySales = JSON.parse(JSON.stringify(this.updateSales));
    }
    const yesterday = new Date(+new Date() - 1000 * 60 * 60 * 24).toISOString().split('T')[0];
    if (updateDate === yesterday) {
      this.yesterdaySales = JSON.parse(JSON.stringify(this.updateSales));
    }
    this.updateSalesDataInit();
    this.showSalesDialog = false;
    this.updateDatePickerUse = false;
  }

  beforeImgUpload(file: any) {
    const isJPGorPNG = file.type === 'image/jpeg' || file.type === 'image/png';
    const isLt10M = file.size / 1024 / 1024 < 10;
    if (!isJPGorPNG) {
      this.$message.error('请上传图片类型的文件');
      return false;
    }
    if (!isLt10M) {
      this.$message.error('上传头像图片大小不能超过 10MB');
      return false;
    }
    return isJPGorPNG && isLt10M;
  }

  imgUploadSuccess(res: any) {
    this.modifyProduct.img = res.data;
    this.$message.success('图片上传成功');
  }

  modifyProductInit() {
    this.modifyProduct = JSON.parse(JSON.stringify(this.product));
  }

  cancelProductUpdate() {
    this.modifyProductInit();
    this.showUpdateDialog = false;
  }

  async submitProductUpdate() {
    let fields = JSON.parse(JSON.stringify(this.modifyProduct));
    fields.type = JSON.stringify(fields.type);
    fields = Object.freeze(fields);
    console.log(fields);
    const result = await this.$store.dispatch(`product/${UPDATE_PRODUCT}`, fields);
    this.showUpdateDialog = false;
    if (result === 'OK') {
      this.$notify({
        title: '更新成功',
        message: '商品信息已更新',
        type: 'success'
      });
      this.product = { ...this.modifyProduct };
    } else {
        this.$notify.error({
          title: '更新失败',
          message: result || '更新失败，请稍后重试'
        });
        this.modifyProduct = { ...this.product };
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
        
        .img-uploader {
          width: 178px;
          height: 178px;
          border: 1px dashed #d9d9d9;
          border-radius: 6px;
          cursor: pointer;
          position: relative;
          overflow: hidden;
          margin-bottom: 10px;    
        }

        .img-uploader:hover {
          border-color: #409EFF;
        }

        .img-uploader-icon {
          font-size: 28px;
          color: #8c939d;
          width: 178px;
          height: 178px;
          line-height: 178px;
          text-align: center;
        }
        .p_info_img {
          width: 178px;
          height: 178px;
          display: block;
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

        .update_sales_footer {
          margin-top: 10px;
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

.sales_detail_table {
  .table_container {
    margin-top: 20px;
    width: 900px;
  }
}
</style>
