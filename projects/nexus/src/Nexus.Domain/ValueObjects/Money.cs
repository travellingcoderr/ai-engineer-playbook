using System;

namespace Nexus.Domain.ValueObjects
{
    public record Money
    {
        public decimal Amount { get; }
        public string Currency { get; }

        public Money(decimal amount, string currency)
        {
            if (amount < 0) throw new ArgumentException("Amount cannot be negative", nameof(amount));
            if (string.IsNullOrWhiteSpace(currency)) throw new ArgumentException("Currency is required", nameof(currency));
            
            Amount = amount;
            Currency = currency.ToUpper();
        }

        public static Money Zero(string currency) => new Money(0, currency);

        public Money Add(Money other)
        {
            if (other.Currency != Currency) throw new InvalidOperationException("Currencies must match");
            return new Money(Amount + other.Amount, Currency);
        }

        public Money Subtract(Money other)
        {
            if (other.Currency != Currency) throw new InvalidOperationException("Currencies must match");
            if (Amount < other.Amount) throw new InvalidOperationException("Insufficient funds");
            return new Money(Amount - other.Amount, Currency);
        }
    }
}
