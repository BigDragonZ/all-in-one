# edX MIS 6-03: DSS hurdles and approaches I

## 元信息

- **序号**: 42
- **课程**: MIS
- **处理时间**: 2026-05-16 12:14:40
- **来源**: 精修版

---

## 精修内容

# edX MIS 6-03: DSS hurdles and approaches I

## 元信息

- **序号**: 42
- **课程**: MIS
- **链接**: https://www.youtube.com/watch?v=rdYeKpwr9UY
- **处理时间**: 2026-05-16 12:13:59
- **来源**: YouTube 自动生成字幕
- **条目数**: 310

---

## 字幕内容

Hello, I hope you are enjoying the sessions. In the previous video, after describing the information systems pyramid—encompassing Transactional Management Information Systems, Decision Support Systems, and the specific type of Decision Support Systems called Executive Information Systems—and highlighting some of the traits of Decision Support Systems, we introduced the topic of the data on which Decision Support Systems rely.

Decision Support Systems (**DSS**), also known as **Business Intelligence** (**BI**) systems, encompass two major components, like any management information system: data and the processing of this data. In Business Intelligence, the processing element involves the data selection, aggregation, and representation we previously discussed, and is referred to in the jargon as **Business Analytics** or merely **Analytics**. Current technology allows for efficient manipulation and intuitive, flexible, user-friendly presentation of data, that is, Business Analytics. Thus, the key challenge faced by Decision Support Systems is obtaining and structuring the appropriate, high-quality data.

In order to better understand this challenge, let us take one step back and ask ourselves the same question about transactional systems, such as the **ERPs** we have been analyzing: where does the data they use come from, both in terms of content and structure? Could you pause the video for a minute and try to answer that question yourself?

Hopefully, you quickly identified where the structure of the data of a transactional system comes from. It is precisely the database data model, which is designed up front by the application developer. In the case of an ERP, it is the data model of the common, shared database, which is, as we discussed, a key ingredient of the ERP. Regarding the content, there are three basic sources:
A. When the system is first installed, reference or structural data or tables are loaded, containing relatively stable data such as organizational units or product lists. These tables are then kept up to date by the system users.
B. Most of the data comes from actually entering the individual transactions, such as keying in customer orders or directly capturing them from the physical world, for example, with a barcode scanner at a checkout counter.
C. As discussed, the data held by an information system for an individual business transaction (say, a customer order) may have to be transferred to the next information system down the line, that is, to the information system supporting the next activity within the business process. In non-ERP environments, this happens all the time. In pure ERP environments, this would not be needed. However, in the real world, even companies adopting ERPs tend to simultaneously use a hodgepodge of complementary information systems, either legacy or specialized in aspects not properly addressed by the ERP.

Thus, in summary, in transactional systems, the data structure is designed in advance by the developers, and data content is basically internally generated through the use of the transactional system and then exchanged among them.

How about Decision Support Systems or Business Intelligence? Taking into account the few broad brushstrokes or hints we have provided about these systems, what do you think their data content and structure would come from? Could I ask you again to pause the video for a minute and try to guess?

Not an easy question, was it? Starting with data content, the first idea that comes to mind is exploiting the data stored in the transactional systems' databases. On the other hand, as discussed in previous videos, there is a broad spectrum of decisions which are likely to have different data requirements. The differences in data requirements imposed by these different types of decisions can be summarized into basic dimensions: functional versus inter-functional integrated data, and internal versus external data.

Structured decisions, operational in nature and typically taken by operational personnel at the base of the pyramid, tend to be quite narrow in focus. Most of the data required to analyze them is internal to the company and thus typically stored within the company's transactional systems' databases. Quite often, all the data required belongs to the same functional area. Thus, even if the company is using individual management information systems rather than a unified ERP, all this data is likely to reside in the database of just one single management information system.

On the other hand, as we move up along the pyramid, wider-ranging decisions increasingly require a broader, multifunctional perspective. As we approach the highest layers, the focus of these increasingly strategic managers shifts outward to the outside of the organization: competition, customers, economic environment. This increasingly requires being supported by data that does not exist within the organization—external data.

Thus, the Business Intelligence infrastructure faces a key challenge: making the data stored in the databases of its various management information systems available for its Decision Support Systems in an integrated manner, and ideally, at the disposal of management, combined with selected, relevant external data.

Before we discuss how companies handle this issue, let us stop for a minute to pose a couple of review questions. Thank you.