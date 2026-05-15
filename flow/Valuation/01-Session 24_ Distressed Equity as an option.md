# Session 24: Distressed Equity as an option

## 元信息

- **序号**: 1
- **课程**: Valuation
- **处理时间**: 2026-05-16 01:21:44
- **来源**: 精修版

---

## 精修内容

Let's say you decide to buy stock in a company that's losing money, that you expect to keep losing money in the future, and has a lot of debt—essentially a basket case company. You might wonder, why would I want to do that? For the same reasons you buy a deep out-of-the-money option. Most of the time, you're going to lose all the money you invested, but some of the time, you're going to make an incredible return. That's the basis for investing in equity in a deeply troubled company. You're investing in an option. In this session, I hope to expand on that concept and look at the implications for investors.

These last three sessions, we've talked about using option pricing in the context of valuation. We've talked about using option pricing to value a young biotechnology company or a natural resource company. In the last session, we talked about using option pricing to value the option to expand and abandon. In this session, I want to wrap things up and talk about a very specific case where option pricing can be your ally in valuing equity.

Step back and think about buying equity in a publicly traded company. Here's what you get: you get a share of ownership in the company. You also get limited liability. You know what that means, right? If the company gets into trouble, you can lose what you paid for the equity, but you cannot be held responsible for anything more. Your stock price can get to zero, but it cannot become negative. So, you have limited liability, and you have the choice—though you might not use it in most companies—to liquidate the company anytime you want. If I use that limited liability and the right you have to liquidate together, I have the makings of an option.

Here's why. Let's assume you're the equity investor in a firm with a value V and some debt outstanding with a face value D. If the value of the business (V) exceeds the debt (D), then when you liquidate the firm, you get the difference, V minus D. If the value of the firm is less than the outstanding debt, remember you have limited liability, so you get zero. That looks very much like a call option. If you replace V with S (the value of the underlying asset) and D with K (the strike price), you have the makings of a call option. If you liquidate a firm as the equity investor, and the value of the assets in liquidation exceeds the face value of the debt, you get to keep the difference. If the value of the assets is less than the face value of the debt, you get nothing. That is the insight we're going to use to value equity in deeply distressed companies.

Let's try this with some real numbers. Assume you have a business that you valued at $100 million. Let's also assume that this company has only one zero-coupon bond outstanding with a 10-year maturity and an $80 million face value. Finally, let's assume that the standard deviation in your value estimate of $100 million is 40%, and the risk-free rate is 10%. That doesn't sound like much information, but I'm going to argue that with that information and an option pricing view of the world, you should be able to tell me how much the equity in this business is worth and what interest rate you would charge on the debt.

To set up this process, I'm going to think about all these numbers in terms of inputs into an option pricing model. The option I'm valuing here is the option to liquidate, which you own as the equity investor.
- The value of the underlying asset (S) is the value of the firm: $100 million.
- The strike price (K) is the face value of the debt: $80 million.
- The life of the option (T) is the maturity of the debt: 10 years. This is because, at the end of the 10th year, the bondholder gets the power to liquidate. I made it a zero-coupon bond to simplify; a regular bond with coupon payments would be like a series of shorter-term options.
- The variance in the value of the asset is the standard deviation squared (0.40^2), which is 0.16.
- The risk-free rate is 10%.

I have all the inputs I need to value the option. I plug them into my option pricing model (I use the Black-Scholes model), and the value that I get for the call option is $75.94 million. If I view equity in this company as an option, it's worth $75.94 million. The overall value of the company is $100 million. Subtracting the equity value gives me a value for the debt of $24.06 million. Remember, that's a zero-coupon bond with an $80 million face value, and its market value today is $24.06 million. With those two numbers, I can back into an interest rate I would charge on the bond, which is 12.77%. The default spread you should be charging is 2.77% (12.77% - 10%).

When you view equity as a call option, some very interesting implications emerge. Let's assume we wake up tomorrow to catastrophic news: half your business has disappeared. It was worth $100 million, and now it's worth only $50 million. Your equity, which was worth $75.94 million, is going to drop in value. You might naively subtract the $50 million loss from the equity value, but you'd be missing something. You still have an option. Let's revalue the option with the new inputs. Most of the inputs remain the same; the one number that's changed is the value of the underlying business, which is now $50 million instead of $100 million. I plug the numbers in and get a new value for the equity of $3.44 million.

The equity value dropped from $75.94 million to $3.44 million, a drop of $72.5 million. Remember, the value of the business only dropped by $50 million. Who else is bearing the loss? The answer is simple: the lender. The debt that used to be worth $24.06 million is now worth only $1.56 million (which is the old value of $24.06 million minus the additional loss of $22.5 million). The lenders are bearing some of the loss.

What follows from this? I took this company and kept dropping the value of the business from $50 million to $40, to $30, to $10, while keeping the $80 million, 10-year zero-coupon bond as is. I was trying to find out: when does equity in a publicly traded company become worthless? The answer is: almost never. In this example, I kept lowering the value, and the equity hung in there. Equity is an incredibly stubborn instrument. What's keeping the value intact is a combination of two things: time and volatility. You have 10 years to play this game, and as long as you have time, the equity will not become worthless.

The implications are very interesting. When you look at stock in deeply troubled companies, don't expect the stock price to go to zero. You will see stock prices stay above zero, and the value of that equity can be explained primarily as an option. This means if you're going to buy equity in a deeply distressed company, you want that company to be in a volatile, risky business, because volatility is your ally.

If you decide to apply this approach to a real company, here are some suggestions for getting the inputs:
1.  **Value of the underlying assets (S):** You can use a conservative discounted cash flow (DCF) valuation, focusing only on existing assets, or use a relative valuation with a low-end EBITDA multiple.
2.  **Strike Price (K) and Maturity (T):** Since most companies don't have a single zero-coupon bond, you'll have to create one. Take all of the debt outstanding, add up the face value of all of it (including future coupon payments) to get a consolidated face value (K). Then, take a weighted average of the maturities of all the debt to get a single maturity (T).
3.  **Variance:** You can use the variance of past stock and bond prices for your company, but that's messy. A simpler way is to use the average variance for the industry your company is in.

In summary, we normally value equity using DCF or relative valuation. But sometimes, if you're valuing equity in a troubled firm, it might pay for you to think of it as an option and value it as such.