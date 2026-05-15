Answer:
# Chapter 18: Activity-Based Costing (ABC) — Deep-Dive Notes

## 1. Definition and Core Concepts
**Activity-Based Costing (ABC)** is an advanced internal reporting system 
designed to provide a more precise allocation of **Manufacturing Overhead 
(MOH)** than traditional methods [1, 2]. While traditional accounting often 
relies on a single "plantwide" rate—typically based on Direct Labor hours or 
machine hours—ABC recognizes that different products consume factory resources 
at varying rates [2, 3].

### Key Theoretical Pillars
*   **The Cost-Benefit Threshold:** Like all managerial accounting, ABC is 
internal and governed by cost-benefit analysis [4]. It is only implemented if 
the improved accuracy of product costing justifies the significantly higher data
collection costs compared to traditional methods [2, 4].
*   **Activity Cost Pools:** Instead of one large overhead bucket, costs are 
segregated into specific "pools" representing distinct activities, such as 
**Purchasing**, **Inspection**, **Machine Setups**, and **Assembly** [5, 6].
*   **Cost Drivers:** These are the causal factors that trigger the incurrence 
of cost [5]. In ABC, managers identify the driver that most accurately reflects 
the consumption of an activity (e.g., number of purchase orders for purchasing 
costs, rather than labor hours) [2, 7].

---

## 2. Mathematical Derivations and Formulas

ABC utilizes a multi-stage allocation process to refine the unit cost of a 
product.

### Stage 1: Determination of Activity Rates
For each identified activity pool ($i$), a predetermined rate is calculated:
$$ \text{Activity Rate}_i = \frac{\text{Budgeted Overhead Cost for Activity } 
i}{\text{Total Budgeted Quantity of Cost Driver } i} $$
*Example: If total inspection costs are $\$32,000$ and the company expects to 
inspect $8,000$ units, the rate is $\$4.00$ per inspection [5].*

### Stage 2: Cost Assignment to Production Runs
Total overhead is allocated to a specific batch or product line based on its 
actual consumption of drivers:
$$ \text{Total Allocated Overhead} = \sum_{i=1}^{n} (\text{Activity Rate}_i 
\times \text{Actual Activity Consumption}_i) $$

### Stage 3: Per-Unit Overhead Calculation
To find the overhead burden per individual unit ($u$):
$$ \text{MOH Cost per Unit} = \frac{\text{Total Allocated Overhead for the 
Run}}{\text{Actual Units Produced in the Run}} $$
*Example: A production run for 2,000 units consuming $\$27,400$ in ABC overhead 
results in a per-unit cost of $\$13.70$ [8].*

---

## 3. Real-world Case Studies

### Tango Company: Transitioning from Volume to Activity
The Tango Company case demonstrates the deconstruction of a generic overhead 
budget into four functional drivers [5, 6]:
1.  **Purchasing:** $\$35.50$ per purchase order.
2.  **Inspection:** $\$4.00$ per unit inspected.
3.  **Setup:** Approximately $\$866.67$ per machine setup.
4.  **Assembly:** Approximately $\$37.33$ per direct labor hour.
By using these granular rates, Tango ensures that a product requiring many 
specialized purchase orders but little assembly labor is not "undercosted" [2, 
6].

### Uniform Company: Precision in Cost Allocation
The Uniform Company case illustrates the application of ABC to a 2,000-unit 
production run [9, 10]. 
*   **Setups:** 4 setups at $\$2,500$ each = $\$10,000$.
*   **Materials Handling:** 30 requisitions at $\$180$ each = $\$5,400$.
*   **Inspection:** 2,000 units at $\$6$ each = $\$12,000$.
The total ABC overhead of **$\$27,400$** provides a far more defensible unit 
cost than a plantwide rate, which would likely ignore the heavy setup and 
requisition costs associated with smaller or more complex batches [8].

---

## 4. Critical Analysis and Limitations

*   **Complexity vs. Utility:** ABC is significantly harder to prepare and 
maintain than traditional costing [2]. It requires constant monitoring of 
non-financial data (orders, setups, inspections) that traditional ledgers do not
always track [2].
*   **Correction of "Product Cross-Subsidization":** Under traditional plantwide
rates, high-volume products often over-absorb overhead, effectively subsidizing 
the complexity of low-volume, specialized products [2, 11]. ABC corrects this by
assigning complexity costs directly to the products that cause them.
*   **Subjectivity in Driver Selection:** While more precise, the choice of a 
cost driver (e.g., using "number of setups" vs. "setup hours") remains a matter 
of professional judgment, which can still lead to slight cost distortions [7].

---

## 5. Cross-chapter Connections

*   **Chapter 14 (Financial Statement Analysis):** ABC refined product costs 
lead to more accurate **Gross Profit Margins** and **Operating Margins**, 
preventing managers from relying on skewed profitability ratios [12, 13].
*   **Chapter 16 (Job Order Costing):** ABC serves as a more sophisticated 
evolution of Job Order Costing [14]. While traditional job costing uses one 
POHR, ABC uses multiple activity rates to populate the overhead section of the 
**Job Cost Card** [8, 9].
*   **Chapter 25 (Relevant Costing):** In "Special Order" or "Make or Buy" 
decisions, ABC allows managers to identify which overhead activities are truly 
**incremental** or **avoidable**, leading to better decision-making than using a
total unit cost that includes unallocated fixed overhead [15-17].

Conversation: 33a91180-30fa-4b1d-af1b-e451ff84889f (turn 1)
