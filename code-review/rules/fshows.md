### 其他

1. 不要滥用 async/await ，用到的地方需要做try catch
2. ts项目不能有any, api接口出入参需要定义
3. 不能有魔法值
4. 需要遵守样式顺序（带有样式校验的项目，无校验的老项目可忽略）
5. 第三方api需要二次封装
6. vue3使用setup语法糖
7. 使用 2 个空格/一个tab 进行缩进
8. 生命周期函数中不要直接写业务逻辑

## 一．编程规约

### (一) 命名规范

#### 1.1.1 命名严谨性

+ <font style="color:#DF2A3F;">严禁使用拼音和中文，使用英文单词全拼或常识性缩写如“DNA、CPU”</font>
+ <font style="color:#DF2A3F;">杜绝完全不规范的缩写，如：</font>`<font style="color:#DF2A3F;">AbstractClass</font>`<font style="color:#DF2A3F;">“缩写”命名成 </font>`<font style="color:#DF2A3F;">AbsClass</font>`

#### 1.1.2 项目命名

<font style="color:#4D4D4D;">全部采用小写方式，以中线分隔。</font>

正例：`fs-ad-management`

反例：`fsAdManagement`

#### 1.1.3 JS、CSS等目录命名【非VUE组件目录】

全部采用 lowerCamelCase<font style="color:rgb(64, 64, 64);"> （</font><font style="color:#DF2A3F;">小驼峰</font>）写法，有复数结构时，要采用<font style="color:#DF2A3F;">复数命名法</font>， 缩写不用复数。

<font style="color:#4D4D4D;">正例：</font>`src/utils/slsTracker.ts`

<font style="color:#4D4D4D;">反例：</font>`src/views/ad-manage/ad-plans/add/index.vue`

#### 1.1.4 常量命名

##### 1) 全大写+下划线

```typescript
const MAX_LENGTH = 200

// 对象里面小写驼峰
export const COMMON_FLAG = {
  yes: 1, // 是
  no: 2 // 否
}
```

##### 2) 表示可见性、进行中的状态

`is + 动词（现在进行时）/形容词`

```json
{
  "isShow": "是否显示",
  "isVisible": "是否可见",
  "isLoading": "是否处于加载中",
  "isConnecting": "是否处于连接中",
  "isValidating": "正在验证中",
  "isRunning": "正在运行中",
  "isListening": "正在监听中"
}
```

##### 3) 属性状态类

```json
{
  "disabled": "是否禁用",
  "editable": "是否可编辑",
  "clearable": "是否可清除",
  "readonly": "只读",
  "expandable": "是否可展开",
  "checked": "是否选中",
  "enumberable": "是否可枚举",
  "iterable": "是否可迭代",
  "clickable": "是否可点击",
  "draggable": "是否可拖拽"
}
```

#### <font style="color:rgb(38, 38, 38);">1.1.5 方法</font>命名

+ <font style="color:rgb(38, 38, 38);">驼峰法</font>
+ <font style="color:rgb(38, 38, 38);">在多数情况下以 </font>**<font style="color:rgb(38, 38, 38);">动词+名词</font>**<font style="color:rgb(38, 38, 38);"> 形式</font>

```typescript
function getUserDetail() {}
```

##### 1) 常用动词

add / update / delete / detail / get

```plain
附： 函数方法常用的动词: 
get 获取/set 设置, 
add 增加/remove 删除, 
create 创建/destory 销毁, 
start 启动/stop 停止, 
open 打开/close 关闭, 
read 读取/write 写入, 
load 载入/save 保存,
begin 开始/end 结束, 
backup 备份/restore 恢复,
import 导入/export 导出, 
split 分割/merge 合并,
inject 注入/extract 提取,
attach 附着/detach 脱离, 
bind 绑定/separate 分离, 
view 查看/browse 浏览, 
edit 编辑/modify 修改,
select 选取/mark 标记, 
copy 复制/paste 粘贴,
undo 撤销/redo 重做, 
insert 插入/delete 移除,
add 加入/append 添加, 
clean 清理/clear 清除,
index 索引/sort 排序,
find 查找/search 搜索, 
increase 增加/decrease 减少, 
play 播放/pause 暂停, 
launch 启动/run 运行, 
compile 编译/execute 执行, 
debug 调试/trace 跟踪, 
observe 观察/listen 监听,
build 构建/publish 发布,
input 输入/output 输出,
encode 编码/decode 解码, 
encrypt 加密/decrypt 解密, 
compress 压缩/decompress 解压缩, 
pack 打包/unpack 解包,
parse 解析/emit 生成,
connect 连接/disconnect 断开,
send 发送/receive 接收, 
download 下载/upload 上传, 
refresh 刷新/synchronize 同步,
update 更新/revert 复原, 
lock 锁定/unlock 解锁, 
check out 签出/check in 签入, 
submit 提交/commit 交付, 
push 推/pull 拉,
expand 展开/collapse 折叠, 
enter 进入/exit 退出,
abort 放弃/quit 离开, 
obsolete 废弃/depreciate 废旧, 
collect 收集/aggregate 聚集
```

##### 2) 事件命名

使用 `on` `handle` 开头命名

```json
{
  "onSubmit": "提交表单",
  "onKeydown": "按下键",
  "handleSizeChange": "处理分页页数改变",
  "handlePageChange": "处理分页每页大小改变"
}
```

### (二) 注释规范

#### 1.2.1 方法注释

必填 `@function` `@param`

```html
/**
 * @function 方法
 * @description 详细描述
 * @author 作者名
 * @param { String } param1 描述
 * @param { [String] } param2 描述
 * @example '['string1','string2']'
 * @return {Number} val
 */
```

#### 1.2.2 常量注释

```html
/**
 * @constant 描述
 */
```

#### 1.2.3 枚举注释

```html
/**
 * @enmu 描述
 */
```

#### 1.2.4 接口注释

```html
/**
 * @api 描述
 */
```

#### 1.2.5 html 注释

+ S: 开始 E: 结束【推荐】
+ Start: 开始 End: 结束【老项目是这种方式，也可以】

```html
<!-- S 弹框 -->
...内容
<!-- E 弹框 -->
```

#### 1.2.6 css 注释

```html
/* 单行注释 */
.title {
  color: #333;
}

/* 模块注释
---------------------------------------------------------------- */
.mod-a {
  color: #333;
}

/**
* @description 文件信息注释
* @author Author Name
* @date 2015-10-10
*/
```

### (三) HTML 规范 （Vue Template 同样适用）

#### 1.3.1 HTML 类型

推荐使用 HTML5 的文档类型申明：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2022/png/134928/1672304943581-d3aebe9b-e718-430f-a4f9-48e738d1c700.png)

**正例：**

```plain
<!DOCTYPE html>
<html>
  <head> 
      <meta http-equiv="X-UA-Compatible" content="IE=Edge" /> 
    <meta charset="UTF-8" /> 
    <title>Page title</title> 
  </head>
  <body> 
   <img src="images/company_logo.png" alt="Company">
 </body> 
  </html>
```

#### 1.3.2 标签

1. <font style="color:rgb(51, 51, 51);">标签必须合法且闭合、嵌套正确，标签名需小写</font>
2. <font style="color:rgb(51, 51, 51);">标签语法无错误，需要符合语义化</font>
3. <font style="color:rgb(51, 51, 51);">标签的自定义属性以</font><font style="background-color:rgb(247, 247, 247);">data-</font><font style="color:rgb(51, 51, 51);">开头，如：</font><font style="background-color:rgb(247, 247, 247);"><a href="#" data-num="18"></a></font>
4. <font style="color:rgb(51, 51, 51);">除非有特定的功能、组件要求等，禁止随意使用id来定义元素样式</font>

HTML5 中新增很多语义化标签，所以优先使用语义化标签，避免一个页面都是 div 或者 p 标 签。

**正例**

```plain
<header></header> 
<footer></footer>
```

**反例**

```plain
<div> 
  <p></p>
</div>
```

#### 1.3.3 引号

使用双引号(" ") 而不是单引号('') 。

正例: `<div c1ass="box"></div>`

反例: `<div class='box'></div>`

### (四) CSS 规范

#### 1.4.1 命名
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2022/png/134928/1672304943630-aac2ebdc-b5a3-48ee-b5bd-0d6e96191830.png)

**不推荐：**

```less
.fw-800 {
  font-weight: 800;
}
.red {
  color: red; 
}


```

**推荐:**

```vue
<template>
  <div class="heavy color-red" id="testId">xxxx</div>
</template>

<style lang="less">
  .heavy {
    font-weight: 800;
  }
  .color-red { 
    color: red; 
  }
  
  .setStyle(@className, @propName) {
      .@{className} {
        @{propName}: @black;
      }
  }
</style>
```

#### 1.4.2 选择器

##### 1) css 选择器中避免使用标签名、 ID 选择器防止污染全局样式

**推荐：**

```css
.my-header { 
  padding-bottom: 0px; 
  margin: 0em; 
}
```

**不推荐：**

```css
#header {
  padding-bottom: 0px; 
  margin: 0em;
}
span {
  color: red;
}
```

##### 2) 使用直接子选择器
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2022/png/134928/1672304943613-530754c1-a60a-4dff-9393-aef09cd4cc35.png)

**推荐:**

```css
.content > .title {
  font-size: 2rem;
}
```

**不推荐:**

```css
.content .title {
  font-size: 2rem;
}

```

#### 1.4.3 精简写法(具体看项目中的配置)

+ 省略 0 后面的单位
+ `,`后面无空格
+ 小数省略`0`
+ 颜色缩写
+ 属性缩写

**推荐：**

```less
div {
  padding: 1em 2em; // 属性缩写
  margin: 0; // 省略 0 后面的单位
  color: rgba(255,255,255,.5); // ,后面无空格
  background: #fff; // 颜色缩写
}
```

**不推荐：**

```css
div {
  padding-top: 1em;
  padding-right: 2em;
  padding-bottom: 1em;
  padding-left: 2em;
  margin: 0em;
  color: rgba(255, 255, 255, 0.5);
  background: #ffffff;
}
```

####

### (五) LESS/SCSS 规范

#### 1.5.1 代码组织

##### 1) 将公共样式文件放置在 /assets/styles 文件夹下

例: // `variables.less`  `common.less`

##### 2) 按以下顺序组织

1. @import
2. 变量声明
3. 样式声明

```css
@import "mixins/size.less"; 
@default-text-color: #333; 
.page {
  width: 960px; 
  margin: 0 auto; 
}
```

#### 1.5.2 避免嵌套层级过多
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2022/png/134928/1672304944173-045a5109-c3a8-4e0a-ab8f-20205a1f0ccd.png)

**推荐：**

```css
.main-title {
  .name { color: #fff; }
}
```

**不推荐：**

```css
.main {
  .title { 
    .name { 
      color: #fff;  
    } 
  }
}
```

### (六) Javascript 规范（StandardJS）

#### 1.6.1 字符串

##### 1) 统一使用单引号('')，不使用双引号(")

**正例:**

```typescript
let str = 'foo'
let testDiv = '<div id="test"></div>'
```

**反例：**

```typescript
let str = "foo"
let testDiv = "<div id='test'></div>"
```

##### 2) 字符串太长的时候，请不要使用字符串连接符换行 \，而是使用 +

```typescript
const str =
  '首展科技 首展科技 首展科技' +
  '首展科技 首展科技 首展科技' +
  '首展科技 首展科技'
```

##### 3) 程序化生成字符串时，请使用模板字符串

```typescript
const test = 'test'
// bad
const str = ['a', 'b', test].join()
const str = 'a' + 'b' + test

// good
const str = `ab${test}`
```

#### 1.6.2 对象声明

##### 1) 使用字面值创建对象

**正例：** `let user = {}`

**反例：** `let user = new Object()`

##### 2) 使用字面量来代替对象构造器

**正例：** `let user = { age: 0, name: 1, city: 3 }`

**反例：**

```typescript
let user = new Object()
user.age = 0
user.name = 0
user.city = 0
```

##### 3）对象中的属性值使用简写

如`job: job` 简写成 `job`，简写方式要和声明式的方式分组

```typescript
const job = 'doctor'
const department = 'FS'

// bad
const item = {
  sex: 'male',
  job: job,
  age: 25,
  department,
}
// good
const item = {
  job,
  department,
  age: 25,
  sex: 'male',
}
```

#### 4）对象中的方法使用简写

```typescript
// bad
const item = {
  value: 1,
  addValue: function (val) {
    return item.value + val
  },
}
// good
const item = {
  value: 1,
  addValue(val) {
    return item.value + val
  },
}
```

#### 1.6.3 使用 ES6+
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2022/png/134928/1672304944124-0e6f85fc-3b1e-41d6-9e91-f15b91dc3d1a.png)

+ 使用 const/let，禁止使用 var

#### 1.6.4 括号
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2022/png/134928/1672304944073-cedb8c91-52c2-4267-8334-7a7db3b1afe9.png)

**正例：**

```typescript
if (condition) { 
  doSomething()
}
```

**反例：**

```typescript
if (condition) doSomething()
```

#### 1.6.5 undefined 判断

永远不要直接使用 undefined 进行变量判断；使用 typeof 和字符串’undefined’对变量进行判断。

**正例：**

```typescript
if (typeof person === 'undefined') { ... }
```

**反例：**

```typescript
if (person === undefined) { ... }
```

#### 1.6.6 条件判断和循环最多三层
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2022/png/134928/1672304944118-290d8470-36e7-4e4b-88fd-6acf98d92f38.png)

```typescript
// bad
if (!x) {
  if (!y) {
    x = 1
  } else {
    x = y
  }
}

// good
x = x || y || 1
```

#### 1.6.7 解构赋值

当需要使用对象的多个属性时，请使用解构赋值

```typescript
// bad
function getFullName(user) {
  const firstName = user.firstName
  const lastName = user.lastName
  return `${firstName} ${lastName}`
}

// good
function getFullName(user) {
  const { firstName, lastName } = user
  return `${firstName} ${lastName}`
}
```

#### 1.6.8 函数

不要使用 `arguments`，可以选择使用扩展运算符`...`

```typescript
// bad
function test() {
  const args = Array.prototype.slice.call(arguments)
  return args.join('')
}

// good
function test(...args) {
  return args.join('')
}
```

不要更改函数参数的值

```typescript
// bad
function test(opts) {
  opts = opts || {}
}
// good
function test(opts = {}) {
  // ...
}
```

#### 1.6.9 函数变量声明

一个声明只能有一个变量

```typescript
// bad
let a, b, c

// good
let a
let b
let c
```

#### 1.6.10 遍历数组的方式

[建议] 推荐使用普通 for 循环，因为速度最快

[建议] for in 遍历对象时, 使用 hasOwnProperty 过滤掉继承的属性。

```javascript
for (var prop in obj) {
  if (obj.hasOwnProperty(prop)) {
    console.log(`obj.${prop} = ${obj[prop]}`);
  }
}
```

### (七) 图片规范

#### 1.7.1 PNG、JPG图片文件命名

全部采用小写方式，以下划线分隔，多<font style="color:rgb(68, 68, 68);">精度图片加上 </font>@2x｜@3x。

```plain
step_cut.png // 1倍图片
step_cut@2x.png // 2倍图片
step_cut@3x.png // 3倍图片
```

#### 1.7.2 png图片需要进行压缩

[https://tinypng.com/](https://tinypng.com/)

## 二、Vue3 项目规范

### (一) Vue 编码基础

#### 2.1.1. 组件规范

##### 1) 命名

+ 多个单词组成（大于等于 2）
+ 大驼峰
+ 基础组件文件名为 Fs 开头
+ 和父组件紧密耦合的子组件应该以父组件名作为前缀命名
+ 单文件组件命名如`FsTodoItem.vue`，如果拆分了 css 部分，如`FsTodoList`，内部使用`index`命名
+ 详情页等子页面放在父业面文件夹下

**正例：**

```plain
components/
  |- TodoList
    |- index.vue
    |- index.scss
  |- TodoListItem.vue（以父组件名作为前缀命名）
  |- UserProfileOptions.vue （完整单词）
|- views/
  |- UserList/
      |- UserDetail.vue
      |- index.vue
      |- index.scss
```

**反例：**

```plain
components/
|- TodoList.vue
|- TodoItem.vue
|- UProfOpts.vue （使用了缩写）
```

##### 2) 在 JSX/TSX使用组件，应使用 PascalCase 模式，并且使用自闭合组件

```html
<!-- 在JSX/TSX的render函数中使用单词大写开头（PascalCase） -->
<MyComponent />

<!-- 在template模板中使用小写字母加横线的方式 -->
<my-component></my-component>
```

##### 3) Prop 定义应该尽量详细

+ 必须使用 camelCase 驼峰命名
+ 必须指定类型
+ 必须加上注释，表明其含义
+ 必须加上 required 或者 default，两者二选其一
+ 如果有业务需要，必须加上 validator 验证

**正例：**

```vue
defineProps（{
  // 组件状态，用于控制组件的颜色
  status: {
    type: String,
      required: true,
      validator: function (value) {
      return [
        'succ',
        'info',
        'error'
      ].indexOf(value) !== -1
    }
  },
  // 用户级别，用于显示皇冠个数
  userLevel：{
    type: String,
    required: true
  }
}）
```

##### 4) 为组件样式设置作用域

**正例：**

```typescript
<template>
  <button class="btn btn-close">X</button>
</template>
<!-- 使用 `scoped` 特性 -->
<style scoped>
.btn-close {
  background-color: red;
}
</style>
```

**反例：**

```typescript
<template>
  <button class="btn btn-close">X</button>
</template>
<!-- 没有使用 `scoped` 特性 -->
<style>
.btn-close {
  background-color: red;
}
</style>
```

##### 5) 如果特性元素较多，应该主动换行

**正例：**

```html
<my-component
  foo="a"
  bar="b"
  baz="c"
  ddx="d"
  eed="e"
  www="f"
/>
```

**反例：**

```html
<my-component foo="a" bar="b" baz="c" ddx="d" eed="e" www="f" />
```

#### 2.1.2. 模板中使用简单的表达式

组件模板应该只包含简单的表达式，复杂的表达式则应该重构为计算属性或方法。

正例：

```typescript
<template>
  <p>{{ normalizedFullName }}</p>
</template>
// 复杂表达式已经移入一个计算属性
computed: {
  normalizedFullName: function () {
    return this.fullName.split(' ').map(function (word) {
      return word[0].toUpperCase() + word.slice(1)
    }).join(' ')
  }
}
```

**反例：**

```typescript
<template>
  <p>
  {{
    fullName.split(' ').map(function (word) {
      return word[0].toUpperCase() + word.slice(1)
    }).join(' ')
  }}
  </p>
</template>
```

#### 2.1.3 指令都使用缩写形式

指令推荐都使用缩写形式，(用 : 表示 v-bind: 、用 @ 表示 v-on: 和用 # 表示 v-slot:)

**正例：**

```typescript
<input
  @input="onInput"
  @focus="onFocus"
/>
```

**反例：**

```typescript
<input
  v-on:input="onInput"
  @focus="onFocus"
/>
```

#### 2.1.4 标签顺序保持一致

单文件组件应该总是让标签顺序保持为 `

**正例：**

```html
<template>...</template>
<script>...</script>
<style>...</style>
```

**反例：**

```html
<template>...</template>
<style>...</style>
<script>...</script>
```

#### 2.1.5 必须为 v-for 设置键值 key

#### 2.1.6 v-show 与 v-if 选择

如果运行时，需要非常频繁地切换，使用 v-show ；如果在运行时，条件很少改变，使用 v-if。

#### 2.1.7 Vue Router 规范

##### 1) 页面跳转数据传递使用路由参数

页面跳转，例如 A 页面跳转到 B 页面，需要将 A 页面的数据传递到 B 页面，推荐使用路由参数进行传参。

vuex中的数据页面刷新会丢失。

正例：

```plain
let id = ' 123';
this.$router.push({ name: 'userCenter', query: { id: id } });
```

##### 2) 使用路由懒加载（延迟加载）机制

```plain
{
    path: '/uploadAttachment',
    name: 'uploadAttachment',
    meta: {
      title: '上传附件'
    },
    component: () => import('@/view/components/uploadAttachment/index.vue')
  },
```

**3) router 中的命名规范**

path、name命名规范采用lowerCamelCase小驼峰命名

```plain
// 动态加载
export const reload = [
  {
    path: '/reload',
    name: 'reload',
    component: Main,
    meta: {
      title: '动态加载',
      icon: 'icon iconfont'
    },
    children: [
      {
        path: '/reload/smartReloadList',
        name: 'smartReloadList',
        meta: {
          title: 'smartReload',
          children: [
            {
              title: '查询',
              name: 'smartReloadSearch'
            }
          ]
        },
        component: () =>
          import('@/views/reload/SmartReload/SmartReloadList.vue')
      }
    ]
  }
];
```

### (二) Vue 项目目录规范

#### 2.2.1 基础

项目目录的命名要与后端命名统一。

比如活动：后端 activity, 前端router , store, api 等都使用 activity 单词

**2.2.2 目录说明**

```plain
src                                  源码目录
|-- api                              所有api接口
|-- assets                           静态资源，images, icons, styles等
|-- components                       公用组件
|-- config                           配置信息
|-- constants                        常量信息，项目所有Enum, 全局常量等
|-- hooks                            hooks
|-- plugins                          插件，全局使用
|-- router                           路由，统一管理
|-- stores                           vuex/pinia
|-- types                            类型定义
|-- layout                           布局文件
|-- views                            视图目录
|-- utils                            公共方法

```

#### 2.2.3 其他

##### 1) 尽量不要手动操作 DOM

因使用 vue 框架，所以在项目开发中尽量使用 vue 的数据驱动更新 DOM，尽量（不到万不得已）不要手动操作 DOM，包括：增删改 dom 元素、以及更改样式、添加事件等。

##### 2) 删除无用代码

对于无用代码必须及时删除，例如：一些调试的 console 语句、无用的弃用功能代码。

#### 2.2.4 顺序

```vue
<script lang="ts" setup>
// import xxx

// 属性等 defineOptions、defineProps、defineEmits

// 变量声明
// hooks
// computed、watch
// 方法

// onMounted
// defineExpose
</script>

```

## 三 接口相关

#### 3.1.1 常用接口字段

| 参数 | 类型 | 默认值 | 描述 |
| --- | --- | --- | --- |
| page | int | 1 | 当前页码；一般出现在请求入参中，需要做列表分页时才有 |
| pageSize | int | 10 | 当前一页多少数据量；一般出现在请求入参中，需要做列表分页时才有，后端有一个默认显示数量，前端可以通过该字段定义数量；非必填 |
| totalCount | int | 0 | 总共有多少条数据； |
| list | Array | [] | 任何一个列表都使用 list 字段，不需要做其他区分；当一下子返回多个列表时候前面加上对应列表名，如 storeList，但是同时返回多个列表的情况很少 |
| username | string | "" | 用户名 |
| password | string | "" | 密码 |
| oldPassword | string | "" | 原始密码 |
| newPassword | string | "" | 新密码 |
| verificationCode | string "" | 验证码 | |
| phone | string | "" | 手机号 |
| headImage | string | "" | 头像 |
| email | string | "" | 邮箱地址 |
| address | string | "" | 地址 |
| province | string | "" | 省份 |
| city | string | "" | 城市 |
| district | string | "" | 地区 |
| hasPermission | int | 1 | 是否拥有权限；1：有；2：没有 |
| isAdmin | int | 1 | 是不是 Admin；1：有；2：没有 |
| time | string | "yyyy-MM-dd HH:mm:ss" | 除了时间段，其他单个时间都使用 time 为字段 |
| startTime | string | "yyyy-MM-dd HH:mm:ss" | 开始时间 |
| endTime | string | "yyyy-MM-dd HH:mm:ss" | 结束时间 |
| status | int | 1 | 对应状态，0 不允许有业务含义；如：1：开启；2：已关闭 |
| searchContent | string | "" 列表筛选条件搜索的内容字段 | |
| version | string | 1.0.0 | 版本号 |
| appinfo | string | { "appVersion":"1.0.0", "clientIp":"127.0.0.1","extendData":{}} | APP 信息（app 专用，不参与验签） |
| sign | string | sad2ewdeqwekqwje910shd | 请求参数的签名串，签名方式：MD5 |

#### 3.1.1 接口返回

| 参数 | 类型 | 默认值 | 描述 |
| --- | --- | --- | --- |
| errorCode | int | 200 | 错误 code；当业务错误时候，前端通过判断 errorCode 执行对应 操作 |
| errorMsg | string | “” | 错误信息；当业务错误时候，前端直接将其展示给用户 |
| data | Object | {} | 接口返回数据的对象；当 success 为 true 的时候，data 必须是一个对象，像一些列表、单个数据等都在 data 中 |
| success | Boolean | false | 该接口业务逻辑是否成功 |

#### 3.1.3 列表响应结构

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| list | Array | 是 | 200 | 列表的字段 |
| totalCount | int | 否 | 0 | 当 PC 端，此字段必须有，因为前端需要做分页；当移动端上拉加载的时候，此字段是不需要的 |
