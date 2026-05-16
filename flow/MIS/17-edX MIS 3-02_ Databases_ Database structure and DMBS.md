# edX MIS 3-02: Databases, Database structure and DMBS

## 元信息

- **序号**: 17
- **课程**: MIS
- **处理时间**: 2026-05-16 11:54:33
- **来源**: 精修版

---

## 精修内容

# edX MIS 3-02: Databases, Database structure and DBMS

## 元信息

- **序号**: 17
- **课程**: MIS
- **链接**: https://www.youtube.com/watch?v=u3dJYGRfVtI
- **处理时间**: 2026-05-16 11:53:42
- **来源**: YouTube 自动生成字幕
- **条目数**: 421

---

## 字幕内容

In this video, we will study data as the raw material used by Information Systems, differentiate the data itself from its processing or manipulation by software programs, and explore its internal structure with the help of an analogy with an automobile repair shop.

The business processes of any company or organization, such as procurement or sales, rely on information and information flows. Information Systems support these information and information flow requirements. Data is the raw material used by Information Systems. The term "data" is normally used to refer to unprocessed, out-of-context sets of numbers or text elements. In a gas station, each fuel dispenser or pump will send a string of data to the indoor sales system. This unprocessed data is of little use. However, once the sales information system has processed this data, added the required context, and converted it, for example, into aggregated sales figures per fuel type and day of the week, it becomes useful information on which business decisions can be based. Some authors even differentiate data, information, knowledge, and wisdom, but we will skip that in this introductory course.

Thus, structure and context are at least as important as the actual values of the data. In order to better understand how data is Information Systems' raw material and to differentiate the data itself from its processing by software programs, we will resort to the analogy of an automobile repair shop or garage.

In the simplified auto garage in our analogy, customers bring their cars and ask a mechanic to carry out some tasks within his or her area of specialization, such as transmission repair. To do that, however, they will have to use the appropriate spare parts. The mechanic will carry out the requested tasks, but to do that, they will need to get and use spare parts. In a management information system, we can also differentiate two basic constituents: programs and data. When a user accesses an information system, they are actually invoking one or several application programs. Application programs, such as those that update the inventory in a warehouse management system, are coded to carry out specialized tasks, as mechanics do. They are software programs developed in programming languages—a series of instructions. However, to carry out the task of updating the inventory in this example, the programs will need to access and possibly update data—the inventory data in this example. Data would correspond to the spare parts, and application programs to the mechanics in our analogy.

In a well-managed garage, its mechanics would not keep their own stock of spare parts. Rather, all spare parts would be stored and organized in a spare parts stockroom. It is worth highlighting that in addition to the spare parts themselves, the stockroom contains the racks, shelves, compartments, and levels that allow spare parts to be properly organized and easily retrievable. The information systems equivalent of this spare parts stockroom is the database. A database comprises a collection of related data (the spare parts) along with its structure definition and organization (the racks, shelves, and levels).

I wonder why databases are always depicted as cylinders? Good question. Databases normally reside in disk drives that nowadays tend to come in rectangular, box-like frames, so it looks somehow incongruent. I remember, however, many years ago while operating server computers with detachable disk packs, these disk packs were cylinders resembling large, heavy, old-fashioned hat boxes. Actually, today's disk drives still contain round platters that make up a sort of cylinder, only it is hidden inside the frame.

In a small garage, mechanics might directly walk into the storeroom and help themselves to the spare parts they need. Beyond a certain size, however, this becomes impractical, and another employee is hired whose skills and duties are different from those of the mechanics: the stockroom clerk or manager. Whenever a mechanic needs spare parts, they will ask the stockroom clerk or manager. The stockroom clerk or manager will then validate the request, and then locate, assemble, and deliver the spare parts.

As we shall discuss in more detail in subsequent videos, the information systems equivalent of the stockroom clerk or manager is the Database Management System, or DBMS. A DBMS is a set of software programs that focus squarely on managing databases and sit in between the application programs and the database itself. Whenever an application program needs to access data in the database, it issues a request to the DBMS programs. The Database Management System will then validate the request and then carry out the required operations on the data in the database.

This allows us to visualize a simplified model of a management information system comprising its users, specialized application programs, the Database Management System software, and its database, which includes both the data itself and its organization and structure.

Let us now go through an example of an access by a user to a management information system, highlighting at each step the equivalence with the repair shop analogy. Assume Tom would like to check in a library information system if a given book is available, and Jane wants to have her car's worn-out brake pads replaced in a garage.

Tom would log into a library system, which means he would execute some of the specialized, library management-oriented application programs that make up the library management information system. He would probably first execute some sort of general menu program, which would then transparently pass control to the appropriate specialized program designed to carry out book availability queries. Jane, meanwhile, would take her car to the garage, interact first with a receptionist or general mechanic that would then redirect her to the appropriate mechanic specialized in brakes.

Once the library program obtains from Tom the details of the book whose availability he wants to check, it would issue a request to the Database Management System for the relevant availability data to be retrieved. The programs that make up the DBMS, which are specialized in managing databases (not in books or libraries), would validate the request, then access the database and retrieve the data on the availability of the specified book. They would then send that data back to the library application program, which would in turn present it to Tom.

Jane's mechanic, meanwhile, would contact the spare parts stockroom manager, who is specialized in managing stock rooms (not in brakes or suspensions). The stockroom manager would then validate the request, locate the brake pad, and give it to the mechanic. The mechanic would then carry out the planned replacement operation and hand the fixed car back to Jane.

Therefore, in this video, we have introduced an analogy with an automobile workshop to illustrate the basic components of a management information system, namely: sets of specialized application programs, the Database Management System software, and the database, comprising both the data and its structure. In subsequent videos, we will continue to use this analogy to discuss how databases and Database Management Systems are used, and we will analyze the challenges and opportunities they pose. Thank you, I will see you there.