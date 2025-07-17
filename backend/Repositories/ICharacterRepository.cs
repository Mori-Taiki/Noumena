
using backend.Models;
using System.Threading.Tasks;

namespace backend.Repositories
{
    public interface ICharacterRepository
    {
        Task CreateCharacterAsync(Character character);
    }
}
