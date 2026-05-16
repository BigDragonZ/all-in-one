# edX MIS 4-08: ERP hands-on session I

## 元信息

- **序号**: 30
- **课程**: MIS
- **处理时间**: 2026-05-16 12:04:36
- **来源**: 精修版

---

## 精修内容

Welcome to this hands-on demo, distributed over two videos, in which we will access a demo instance of a real ERP. This demo has several general objectives. It will exemplify, in a real-life case, several concepts discussed in previous sections, such as Software as a Service, client-server, open source, and database management systems. It will also illustrate the general structure of an integrative ERP, encompassing multiple functional modules, and it will give you a certain feeling for how management information systems, and specifically ERPs, look.

However, its main objective is to highlight how ERPs allow specialized tasks from several functional modules to be executed seamlessly on each individual transaction. We will do this by tracing an individual transaction—a customer order—through the multi-function order fulfillment business process.

As you can see in the references included in the complementary material for this section, there are many commercial, proprietary ERP systems to choose from, such as the already-mentioned SAP ERP, Microsoft Dynamics Navision, or Oracle E-Business Suite.

There are also several open-source solutions, such as the one we will use in this session: Odoo. Odoo, formerly named OpenERP and before that TinyERP, is an open-source ERP including various modules such as accounting, sales, manufacturing, and warehouse management. Its modules are developed in the Python programming language. As discussed in previous sessions, it utilizes an existing open-source database management system called PostgreSQL.

Thus, if you feel brave enough, you can access their website, download and install the Odoo software and the PostgreSQL database management system on your computer, configure the whole thing, and give it a go. It may not, however, be all that simple. Before you attempt it, I would certainly advise you to carefully review the next section of this course, particularly the areas of configuration and parameterization.

There is, however, an easier alternative. Like many other ERPs, Odoo is also offered as Odoo Online, which is exactly what we described in previous sections as Software as a Service (SaaS). As you might expect, in this case, the service provided is not free. If you want to use it, you will have to pay a monthly fee linked to the number of modules and users.

Of particular interest for this course is the fact that Odoo also offers what they call "Demo Instances". They are useful to simply get a quick idea of Odoo or, in our case, to get a quick idea of what an ERP looks like and what it can do. These are shared instances that only live for a few hours and can be used to browse around and try things out. Demo instances require no local installation, just a web browser. These demo instances are already configured (as we shall discuss next week) and are loaded with dummy data from a fictitious company.

We shall therefore start by accessing the Uniform Resource Locator (URL) `demo.odoo.com`, which will redirect us to the webpage. Here we can see the top menu, or, if you will, the list of modules that this fictitious company has installed. Even though this is a demo instance and the data we introduce will be erased shortly afterwards, what we're accessing now is real software, as if we were using the actual product in a real setting.

We can easily notice that the various modules span several functional areas, denoting that we are using an ERP. You can, for example, spot modules supporting Sales, Inventory, Accounting, and so on. By clicking on any of them, we can eventually drill down to more specific menus, as you can see in the top bar menu. One of the options within the Inventory module is Inventory Control. Within its pull-down menu, we can select the 'Products' option. This instructs the appropriate programs within the Inventory module to retrieve data on the various products from the database (through the PostgreSQL database management system) and display it in aggregate form. We can go deeper by selecting a specific product, such as the iPad mini, and checking how many units are available.

Thus, in this first video, we have described the environment based on a real ERP in which this demo takes place and used it as an illustration of various concepts presented in previous sections. By actually accessing this demo environment, we have shown the integrated nature of the ERP and how we can drill down to successively more detailed menus and actions.

In the next video, we will illustrate how ERPs support integrated business processes by following an individual business transaction—a customer order—from its inception until its completion. Don't miss it, I will see you there.