using System;
using Nexus.Domain.ValueObjects;

namespace Nexus.Domain.Entities
{
    /// <summary>
    /// REPRESENTATION: Domain Entity (DDD)
    /// This follows the "Rich Domain Model" pattern where behavior stays with the data.
    /// </summary>
    public class Account
    {
        // 1. PROPERTIES (Private setters to enforce encapsulation)
        public Guid Id { get; private set; }
        public string AccountNumber { get; private set; }
        public string OwnerName { get; private set; }
        public Money Balance { get; private set; }

        /// <summary>
        /// REQUIREMENT: EF Core Persistence Constructor
        /// This is required for EF Core to instantiate the entity from the database.
        /// We use null! to satisfy nullable reference checks, knowing EF Core will populate these.
        /// </summary>
        private Account() 
        {
            AccountNumber = null!;
            OwnerName = null!;
            Balance = null!;
        }

        /// <summary>
        /// REQUIREMENT: Domain Constructor
        /// This is the only way for the application to create a new, valid account.
        /// It enforces business rules (like non-null names) from the start.
        /// </summary>
        public Account(Guid id, string accountNumber, string ownerName, Money initialBalance)
        {
            Id = id;
            AccountNumber = accountNumber ?? throw new ArgumentNullException(nameof(accountNumber));
            OwnerName = ownerName ?? throw new ArgumentNullException(nameof(ownerName));
            Balance = initialBalance ?? throw new ArgumentNullException(nameof(initialBalance));
        }

        // 2. BEHAVIOR (Domain methods instead of property setters)
        public void Debit(Money amount)
        {
            // Business Rule: Money objects handle their own subtraction logic/validation
            Balance = Balance.Subtract(amount);
        }

        public void Credit(Money amount)
        {
            // Business Rule: Money objects handle their own addition logic
            Balance = Balance.Add(amount);
        }
    }
}
