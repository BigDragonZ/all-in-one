# edX MIS 6-04: DSS hurdles and approaches II

## 元信息

- **序号**: 43
- **课程**: MIS
- **处理时间**: 2026-05-16 12:15:42
- **来源**: 精修版

---

## 精修内容

# edX MIS 6-04: DSS hurdles and approaches II

## 元信息

- **序号**: 43
- **课程**: MIS
- **链接**: https://www.youtube.com/watch?v=K9R8ZwHaoe8
- **处理时间**: 2026-05-16 12:14:46
- **来源**: YouTube 自动生成字幕
- **条目数**: 375

---

## 字幕内容

To tackle this challenge, an approach taken by many companies is the creation of a data warehouse. Relevant data from the databases of the various transactional systems is periodically extracted and loaded into this data warehouse to keep its contents reasonably current, even though they would not contain totally up-to-date data. Business analytics software and tools are then used to exploit this data.

But why is it so difficult to combine data coming from different Information Systems? Is it due to technical details such as different file formats, and can't technicians sort out these bugs? I agree it is surprising and frustrating to learn that something apparently as simple as combining data from several databases can prove to be so hard.

Given both the technological wonders we witness every day and the relentless hype with which technology companies continuously bombard us with impossible claims regarding what their tools can magically and effortlessly achieve, the explanation highlights a more general rule: the main challenges in information systems are nowadays generally not technological. They tend to be related to either business issues or logical structure issues. Extracting information is currently not a major issue. The main challenge here is the adaptation of the disparate data models of the source transactional Information Systems to the common data model of the data warehouse.

Sometimes, integrating all the data required for the organization's decisions and exploiting this huge repository directly is not practical. Then, subsets of the data warehouse's data of interest for particular groups of users or business units are extracted into smaller data marts, which are then exploited by these users.

As you can deduce from this discussion, the implementation of business intelligence in a company is highly influenced by the approach taken at the transactional level, namely whether they have adopted an ERP approach. In companies using ERPs, decisions requiring a multi-functional perspective could be supported with just the data stored in the ERP's database.

Thus, depending on the nature of the decision to be taken, decision-makers are supported by the decision intelligence infrastructure in different ways. At one end of the spectrum, highly structured, routine, programmed decisions requiring data contained in just one transactional management information system are usually coded in the application programs. If system-calculated decisions require manual confirmation, this step is also coded, as in the Material Requirements Planning (MRP) example. In semi-structured decisions, users apply business analytic tools—running from simple, flexible reporting tools to sophisticated systems encompassing simulation capabilities—to the required data.

I do not understand. Why should we go through all the hassle of moving data from transactional systems to decision support systems? I have a better idea: let us interrogate the transactional system directly. Simply add some programs that allow users to ask meaningful questions to the system databases.

That's a good point, and sometimes companies actually do that. In most cases, however, it is impractical. Depending on the complexity of the user queries and on whether the required data is stored in just one database or spread over several, let us review the various alternatives. If the decision requires data spread over the databases of more than one transactional management information system, this necessarily involves a complex, challenging consolidation step into a data warehouse and/or data marts, as discussed above.

In other cases, the data required for the decision is confined to a single function and is therefore available in the database of just one management information system. Or, it does require a multifunctional perspective; however, since the company is using an integrated ERP, it could be supported with just the data stored in the ERP's database. In these cases, we could either apply our business analytics tools directly on the management information system's database or follow the general model and extract data to a copy—a data warehouse or data mart—which is then exploited.

Without getting bogged down in the technical details, let us just say that the way databases are organized in transactional systems is optimized for recording transactions, but not for applying analytics. Simple reports are no problem, but complex queries could bring an ERP's database to its knees, thus infuriating a large number of transactional users.

Thus, transactional systems such as ERPs typically include a simple module called "Queries," "Reporting," or something similar. Users that only need a simple, reasonably standard view of the data can use them directly on the transactional database. This is also the only option if decisions require data that is absolutely correct and up-to-the-minute. However, for more complex analysis, data is normally extracted, and the analysis is carried out on a copy.

On the other hand, if many of the company's decisions solely require data from the ERP's database, then even though the extraction process is still necessary, the key challenge mentioned above is greatly simplified. Since all data comes from the same database and thus from the same data model, there is no need for cumbersome data model conversions. The business intelligence modules offered by many ERPs take this approach: they carry out regular extractions from the ERP's transactional database and execute their analytics on this shadow, generally summarized database, thus preventing any interference with the production ERP.

As we move upwards towards the top of the pyramid, the inter-functional integration challenge is compounded by the need to incorporate data from external sources. In this regard, as opposed to transactional systems, business intelligence systems do not generate the data they use. Thus, they exploit data generated by their transactional systems and/or external data.

Business analytics could theoretically be run on the database of transactional systems if they encompass all the required information, as is often the case in companies using ERPs. However, for efficiency reasons and to avoid interfering with transactional users, even in this case, companies usually resort to extracting data to replicated databases, data warehouses, and/or data marts, and then exploit this data through business analytics.

Thank you. See you in the next video.