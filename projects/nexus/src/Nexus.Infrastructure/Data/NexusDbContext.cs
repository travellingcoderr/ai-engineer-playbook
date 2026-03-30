using Microsoft.EntityFrameworkCore;
using Nexus.Domain.Entities;
using Nexus.Domain.ValueObjects;

namespace Nexus.Infrastructure.Data
{
    public class NexusDbContext : DbContext
    {
        public NexusDbContext(DbContextOptions<NexusDbContext> options) : base(options) { }

        public DbSet<Account> Accounts { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            var accountBuilder = modelBuilder.Entity<Account>();
            
            accountBuilder.HasKey(e => e.Id);
            accountBuilder.Property(e => e.AccountNumber).IsRequired();
            accountBuilder.Property(e => e.OwnerName).IsRequired();
            
            // Value Object Mapping: Simple implementation for demo
            accountBuilder.OwnsOne(e => e.Balance).Property(p => p.Amount).HasColumnName("BalanceAmount");
            accountBuilder.OwnsOne(e => e.Balance).Property(p => p.Currency).HasColumnName("BalanceCurrency");
        }
    }
}
