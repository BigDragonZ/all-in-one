# edX MIS 6-05: DSS, non-structured data and Big Data. Analytics

## 元信息

- **序号**: 44
- **课程**: MIS
- **处理时间**: 2026-05-16 12:17:01
- **来源**: 精修版

---

## 精修内容

# edX MIS 6-05: DSS, non-structured data and Big Data. Analytics

## 元信息

- **序号**: 44
- **课程**: MIS
- **链接**: https://www.youtube.com/watch?v=fS3iG4n7qYg
- **处理时间**: 2026-05-16 12:15:47
- **来源**: YouTube 自动生成字幕
- **条目数**: 396

---

## 字幕内容

In previous videos, we have analyzed what we could call conventional business intelligence. Simple, repetitive, highly structured decisions were handled by specific programs or modules within the transactional systems, working directly against the transactional databases. Actually, many people would not even call this business intelligence. To support less structured decisions, selected information was periodically extracted from the databases of one or several of the company's transactional systems. These extracts, along with in some cases additional external data, were then combined and loaded into reporting-oriented databases: data warehouses, data marts. Business analytics were then run using the appropriate software on these ad-hoc databases.

Along these discussions, we have implicitly assumed that data used to support decisions was structured data, similarly to data used in transactional systems. Thus, we knew the data's data model. Increasingly, however, companies are trying to harness the power of unstructured data.

Could you explain what you mean by unstructured data? Data is always highly structured, right? And in case it didn't have a structure, wouldn't it be hopelessly useless? Well, not quite. Things are not that simple.

Let us start by reviewing what structured and unstructured data mean. Please note that the concept of structured data, even though related, is not identical to the concept of structured decisions. In structured data, data is neatly formatted, organized in well-defined fields and tables, and their relationships among tables are known. Data in transactional databases such as customer orders, inventory levels, employee salaries, and manufactured quantities is fully structured. Therefore, the reporting-oriented decision support systems databases we build by combining extracts from these databases are similarly structured. Programs used to analyze this data can rely on knowing the data structure or data model. For example, the decision support systems programs could calculate the total sales amount for any given customer last year because all related data conforms to a known data model. Like this, all sales transactions would be stored in identical records, the amount and date fields would be known and their format understood, and the link or relationship through a foreign key between the sales records in the sales table and the customer records in the customer table would also be known. Exploiting structured data is like retrieving materials from a properly organized warehouse.

On the other hand, as we discussed when we first introduced the concept of Big Data, this traditional structured data, mostly internal to the organization, is being overshadowed for decision support purposes by a new breed of data, mostly external to the organization or at least to its data center. The term Big Data was coined to refer to these massive, cumbersome sets of ill-structured data coming from various sources such as social media, the web, or machine-generated data like data coming from the Internet of Things. Thus, the challenges involved in unveiling Big Data's hidden treasures do not stem merely from its sheer size, but also from its lack of structure. Most of this data is coming in as raw, unstructured text from social media (thus the so-called social media mining), tracking devices, sensors, intelligent RFID labels, and large audio and image files. This unstructured or semi-structured data is much harder to analyze, aggregate, and generally speaking, make sense out of. This poses tricky challenges for both the storage, retrieval, and manipulation of this data via business analytics.

Isn't 'analytics' just a fancy word for what has been known for decades as 'data mining'?

Well, I have also been around for decades, thus I actually like the 'data mining' term. If, as we said, exploiting structured data is like retrieving materials from a properly organized warehouse, exploiting unstructured data is much more like mining. It involves digging out large amounts of ore (or raw data) looking for hints of valuable information, the precious metal: hidden underlying patterns, any regularities that can be used to explain or predict, and thus make better decisions and gain competitive advantage. Nevertheless, you can't avoid the tech industry's fixation with continuously creating fancy labels. Besides, the order of magnitude change experienced in both the data involved and the sophistication of the tools used to manage it probably justifies a new term.

In previous videos, we focused mainly on the new tools and approaches aimed at handling vast amounts of data, such as the Apache Hadoop distributed computing framework or in-memory database management systems. These advancements in the 'data leg' are complemented with equally stark advances in the 'manipulation leg': business analytics, including predictive analytics, prescriptive analytics, web analytics, and even specialized niches such as fraud analytics. These tools can effectively manage both structured data and can also be used in conventional decision support systems and for unstructured Big Data.

I do feel there is a lot of hype in all this Big Data craze. Could you give a few specific hints on what makes Big Data any different from 'business as usual'?

In my personal opinion, this is more an evolution than a completely different