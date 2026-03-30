using System;
using System.Linq;
using Nexus.Domain.Entities;
using Nexus.Domain.ValueObjects;

namespace Nexus.Infrastructure.Data
{
    public static class DbInitializer
    {
        public static void Initialize(NexusDbContext context)
        {
            context.Database.EnsureCreated();

            if (context.Accounts.Any()) return;

            var accounts = new[]
            {
                new Account(Guid.NewGuid(), "1001", "Alice Rogers", new Money(1000, "USD")),
                new Account(Guid.NewGuid(), "1002", "Bob Smith", new Money(500, "USD")),
                new Account(Guid.NewGuid(), "1003", "Charlie Brown", new Money(2500, "USD"))
            };

            context.Accounts.AddRange(accounts);
            context.SaveChanges();
        }
    }
}
