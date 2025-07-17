
using backend.Models;
using Neo4j.Driver;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

namespace backend.Repositories
{
    public class Neo4jCharacterRepository : ICharacterRepository
    {
        private readonly IDriver _driver;

        public Neo4jCharacterRepository(IConfiguration configuration)
        {
            var uri = configuration["Neo4j:Uri"];
            var user = configuration["Neo4j:User"];
            var password = configuration["Neo4j:Password"];
            _driver = GraphDatabase.Driver(uri, AuthTokens.Basic(user, password));
        }

        public async Task CreateCharacterAsync(Character character)
        {
            var session = _driver.AsyncSession();
            try
            {
                await session.ExecuteWriteAsync(async tx =>
                {
                    var query = @"CREATE (c:Character {id: $id, name: $name, llm_provider: $llm_provider, 
                                    personality: $personality, background: $background, 
                                    values: $values, emotions: $emotions, desires: $desires})";
                    await tx.RunAsync(query, new { 
                        id = character.Id,
                        name = character.Name, 
                        llm_provider = character.LlmProvider,
                        personality = character.Personality,
                        background = character.Background,
                        values = character.Values,
                        emotions = character.Emotions,
                        desires = character.Desires
                    });
                });
            }
            finally
            {
                await session.CloseAsync();
            }
        }
    }
}
