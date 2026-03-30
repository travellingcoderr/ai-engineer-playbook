using System;
using System.Threading.Tasks;
using Nexus.Domain.Entities;

namespace Nexus.Domain.Repositories
{
    public interface IAccountRepository
    {
        Task<Account?> GetByIdAsync(Guid id);
        Task UpdateAsync(Account account);
        Task<Account?> GetByAccountNumberAsync(string accountNumber);
    }
}
