# edX MIS 2-05: Distributed Infrastructures. Wide Area Networks (WAN)

## 元信息

- **序号**: 12
- **课程**: MIS
- **处理时间**: 2026-05-16 11:50:16
- **来源**: 精修版

---

## 精修内容

# edX MIS 2-05: Distributed Infrastructures. Wide Area Networks (WAN)

In the previous video, we introduced the concept of **Local Area Networks (LANs)**. We will now discuss how to use these local area networks to access more complex networks spanning larger areas, referred to as **Wide Area Networks (WANs)**. Examples of wide area networks would include the internal private network of a multinational corporation or, as we will discuss later, the Internet.

Wide Area Networks will thus include local area networks and the links interconnecting them. Local area networks will connect to wide area networks through appropriate networking gear, such as **routers**. Routers will analyze the networking traffic within a local area network—that is, the data being sent by the local area network's nodes—and decide whether it should be kept within the local area network because it is a dialogue exclusively among nodes internal to it, or whether it should be routed through the wide area network towards its ultimate destination.

In privately owned wide area networks, such as the private network of a multinational company, the nodes and the local area networks would normally belong to that owner. However, the interconnecting long-distance links are normally rented from specialized telecommunication companies. These long-distance lines, as well as a growing proportion of local area networks, are generally based on optical fibers, which provide much higher capacity than cables or wireless approaches.

The best-known wide area network is the **Internet**. Actually, rather than a network as such, the Internet is a network of networks: local area networks and wide area networks throughout the world. Each of them, belonging to its owner, are linked together through infrastructures provided by specialized companies called **Internet Service Providers (ISPs)**. The largest **Tier 1 ISPs** operate the Internet's backbones: high-capacity fiber optic networks spanning the world, supporting the ever-growing Internet traffic.

These concepts allow us to better understand what is really going on in our daily routines. An employee at her workplace will normally have a device such as a PC, a tablet, or a smartphone, where she can locally carry out some tasks such as editing text. This device will be hardwired (that is, connected via cable) or wirelessly connected (usually through Wi-Fi) to the company's local area network, normally Ethernet-based. Through this local area network, the employee can access other nodes and services residing in the same location. Transparently for the user, if she requires a service that requires interaction with a node within the company's internal network but residing in another location, that request will be routed through the local area network's router, across rented long-distance links, until it reaches the destination node. If the request requires access to nodes in the Internet beyond the company's private network, it will similarly be routed through the company's connections with the Internet Service Providers it has contracted with. The Internet Service Provider will then route the request—for example, a request for a page from a web server which does not belong to the company—to the appropriate destination.

If working from home, the employee might have contracted with an ISP for internet access, typically based on existing telephone lines (DSL), cable, or fiber. The ISP will then connect this communication medium through a router to a small local area network at the employee's house. To this network, the various nodes—PCs, smartphones, and so on—can be connected, as previously discussed, either through Wi-Fi or directly via cables. This allows the employee, while at home, to access either other devices in her home local area network or to access the wider Internet. Provided the company's security measures allow it, she can also then access her company's internal network through the Internet and use it almost as if she was working from her workplace.

Thus, in this section, we have discussed the computer networks that underpin distributed computer infrastructures and decouple users from the underlying information systems. After presenting how several nodes such as PCs, servers, or smartphones can be linked together in local area networks, we have introduced wide area networks. This encompasses both the internal private networks of corporations and other organizations, and the network of networks that is the Internet. Based on these concepts, in the next videos, we will discuss the cloud approach to distributed infrastructures and the benefits it can provide.