# edX MIS 4-09: ERP hands-on session II

## 元信息

- **序号**: 31
- **课程**: MIS
- **处理时间**: 2026-05-16 12:05:29
- **来源**: 精修版

---

## 精修内容

# edX MIS 4-09: ERP hands-on session II

## 元信息

- **序号**: 31
- **课程**: MIS
- **链接**: https://www.youtube.com/watch?v=bwToNlYieDE
- **处理时间**: 2026-05-16 12:04:43
- **来源**: YouTube 自动生成字幕
- **条目数**: 464

---

## 字幕内容

Welcome to this session, in which we will complete the hands-on demo initiated in the previous video. Having described the general setting and the general structure of the ERP, we will now illustrate how ERPs support integrated business processes. We will take the prototypical example of the order fulfillment integrative process. We shall follow an individual business transaction, a customer order, throughout its life cycle, moving along the sequence of related tasks that make up the business process. This will imply that the customer order crosses various functional areas and therefore various ERP modules.

As it concerns a customer order, we will start with a customer. That customer happens to be interested in the product whose availability we checked in the last video: an **iPad Mini**.

"Oh good, I would also like to get an iPad for myself. Maybe I can learn how to trick the ERP into sending an extra unit to me."

"I am afraid ERPs are notoriously hard to trick. You could have an extra unit sent to you, but as we will see, that would also trigger an invoice, which you might not appreciate."

Let us go back to the initial screen's top menu or list of modules. Let us click on the **Inventory** icon or module to drill down to more specific menus. To view the products available in this demo company, we will choose **Inventory Control** and then **Products**. Out of this list of existing products, we will select the **iPad Mini** to check availability. The screen shows that there are 300 units on hand (that is, physically in the warehouse) and a forecasted stock of 137 units. The difference is probably due to outstanding delivery orders for 163 units.

Back to the main or top menu, we will now select the **Sales** module. Let us now create a quotation, or sales proposal, or offer for one of our existing customers, the infamous **Alfonso Duran**, which had previously been added to the customers table in the database. To create the quotation, we must add in successive order lines the products, the **iPad Mini** in our case. We will introduce a 5% discount and an ordered quantity of 10 units. We will leave the tax rate at the default value of 15%. This is the quotation or sales proposal. We will save it and then email it to the customer, whose email was already in the database within the customer's profile, and then click send.

Now that we, as sales representatives, have sent the quotation, please allow me to impersonate the customer, **Alfonso Duran**, for a minute. I am **Alfonso Duran**, and I am reading my mail. I have received a mail from someone called "Administrator" (the sales rep) containing this quotation. I can review it in PDF. Here it is. If I like it, I can go back to the email's main body and follow the link it provides to access this same quotation online, but on the selling company's ERP. By clicking on the link, I am redirected to the selling company's ERP. While it loads, I hope you are mentally reviewing our discussions on networks to figure out what's going on underneath these screenshots.

Here I can see the same quotation, but on the selling company's system, which might in a real case be located either on its premises or in the cloud. Since I, customer **Alfonso Duran**, am at this point actually working within the selling company's ERP, I can now accept that proposal. Thus, I will accept the quotation with my name and signature. The quotation now becomes a firm order.

Okay, end of the impersonation. We are once again the sales reps of the selling company. We are happy that our ERP is telling us that our customer, **Alfonso Duran**, has accepted our quotation for 10 iPads. We therefore select in the drop-down menu to move on to the **Sales Orders** screen. And here we can see the sales orders, including this one shown here.

We can always go back to the main menu by clicking on the top left icon, and we'll go back to the **Inventory** module. This initial inventory screen highlights "things to do," among them three outstanding delivery orders. By clicking on them, we drill down and can see the detail: the three outstanding delivery orders, including ours to be delivered to **Alfonso Duran**.

Let us now check again: how many iPads do we have in inventory? We can see here that we have the same on-hand number as before, 300. However, the forecasted stock has gone down from 137 to 127. Why? Hopefully, you realized this is because we just created a new delivery order for 10 units, meaning that 10 of the units currently in the warehouse are now committed for a customer.

As you can see, we are now witnessing how an individual business transaction, a customer order, is traveling along the tasks that make up the order fulfillment inter-functional business process, thus hopping from functional module to functional module. In contrast to the cumbersome transfer across independent Information Systems in the traditional approach, within this ERP, these transitions take place seamlessly. This is thanks to the individual transaction residing in the common, shared database, like a car in a shared garage or warehouse.

Back to the dashboard, we shall execute our own transaction out of these pending delivery orders. Thus, we will deliver the 10 units requested, which are available in inventory. We'll edit the order and specify how many units will be delivered now. We save and validate it.

Now, in the **Sales** module, we can invoice the order. This is the quotation template out of which we will generate the invoice. We create the invoice. This is the draft invoice. Let's validate it, and now we'll email it again to the customer, **Alfonso Duran**. Here it is.

Now, let me impersonate the customer, **Alfonso Duran**, once again. I am now accessing his mail account. He has the invoice in his inbox. I can see it as an attachment. Since this is a demo, I cannot make an online payment. Thus, I quit my role as **Alfonso Duran** and go back to the ERP as "Administrator," the sales rep, and register the payment. We tell the system that the payment has taken place.

Now we go back to the modules menu, to the **Accounting** module, to show the resulting accounting entries. Within **Journal Entries**, we search and see the two steps in which the transaction has been recorded. The first step was logged before we actually got the money; its double entry used "Accounts Receivable" to indicate that the customer owed us money. And once we collected the money, we logged the next double entry, reflecting that the customer has paid the outstanding amount.

This illustrates why the order fulfillment process we have shown is sometimes called "quote-to-cash." As you can appreciate in this demo, our customer order has completed the integrated, multi-function order fulfillment process without ever leaving the ERP. This highlights how ERPs allow specialized tasks from several functional modules to be executed seamlessly on each individual transaction. Data about that transaction was stored in a normalized, non-redundant manner in the shared ERP's database, where it could be accessed and gradually built upon by the specialized programs of the various modules. This non-redundancy prevented the risk of inconsistencies and ensured that all the modules always access up-to-date data.

Hopefully, this demo, which concludes this week's videos, will facilitate the assimilation of the concepts discussed throughout the week and in previous years. As previously discussed, the advantages that stem from the ERP approach come with a cost in terms of complexity and a certain risk of inflexibility. Next week, we will discuss how to tackle these issues and, particularly, how to address potential differences between the design of our current business processes (how we work) and the design that is somehow implicit in the system (how the ERP expects us to work). Thank you, I hope I will see you there.