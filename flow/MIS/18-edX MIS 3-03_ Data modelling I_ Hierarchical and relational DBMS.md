# edX MIS 3-03: Data modelling I. Hierarchical and relational DBMS

## 元信息

- **序号**: 18
- **课程**: MIS
- **处理时间**: 2026-05-16 11:55:14
- **来源**: 精修版

---

## 精修内容

# edX MIS 3-03: Data modelling I. Hierarchical and relational DBMS

## 元信息

- **序号**: 18
- **课程**: MIS
- **链接**: https://www.youtube.com/watch?v=bJcVGdMB2Jk
- **处理时间**: 2026-05-16 11:54:40
- **来源**: YouTube 自动生成字幕
- **条目数**: 247

---

In the last video, we differentiated within a management information system the specialized application programs, the database management system, and the database itself, encompassing both the data and the way in which data is organized. We will now further discuss this concept of data organization, or structure, or data modeling as it is actually called, and illustrate it with the same car repair shop analogy.

Before data can be stored in a database, it must be logically structured or organized. This process is called data modeling, and the resulting structure is referred to as a data model. Spare parts in the stockroom must similarly be organized, and there are various alternative approaches to do that. For example, parts could be organized according to size, according to car models, according to how frequently they are used, or by grouping together parts that are normally used in the same maintenance operations. The way parts are organized would in turn influence how the stockroom clerk manages them, determining, for example, how they are located and retrieved.

There are also several distinct approaches to structuring and modeling data, and consequently, different types of database management systems. In the initial stages of computing, data used to be organized hierarchically in simple, tree-like pyramidal structures, resembling a traditional company's organization chart. So-called hierarchical database management systems were developed to manage hierarchical databases. An example of the stockroom's equivalent of a hierarchical organization would be to separate spare parts according to the car subsystem they belong to, such as engine, drivetrain, and steering system. Within each subsystem, they would be further classified. For example, drivetrain parts would be classified into gearbox parts, rear and front axle parts, and so on. Analogously to the single line of command in hierarchical organizations, in the hierarchical stockroom of our example, as in hierarchical data structures, there is a single path or way to find a given part or data element.

These initial hierarchical models and database management systems were simple and efficient but quite inflexible. Thus, they have been almost completely replaced by the so-called relational databases and relational database management systems. Thus, even though there are various other types of database management systems, the databases in the information systems in your company are most likely to be relational. Most of the database management system names you may have heard, such as Oracle, MySQL, or even your PC's Microsoft Access, are in fact relational.

In a relational structure, data is organized in tables. For example, a simple database for an automobile insurance company could contain three tables: cars, insurance policies, and drivers. A table contains rows and columns, like the tables that we build on spreadsheets often do. All rows contain the same columns. Each column contains the value of a given attribute, or trait, or field for the individual represented in that row. In our example, each row in the cars table would correspond to a car. The first column could be the license plate.

A table must have a column or attribute that is not repeated and thus identifies the row or individual. This attribute is called the primary key, like the license plate in our example of the car table. Other columns might include the year of manufacture or the car model. The insurance policies table could use the insurance policy code as the primary key and contain other columns such as validity date or fee. The driver's table could have the driver's license number as the primary key and contain other columns such as the driver's age, sex, or address, and a picture.

And yes, databases might contain other digital information formats besides text and figures.

Each row in the insurance policies table would correspond to an individual insurance policy. Each row in the driver's table would correspond to an individual driver. Having discussed how data is organized in tables in a relational model, let us now review these concepts through some short quizzes before we discuss in the next video how these tables are related. I will see you there.