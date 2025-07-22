
using backend.Models;
using Neo4j.Driver;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using System.Text.Json;
using System.Linq;

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
                        values = JsonSerializer.Serialize(character.Values),
                        emotions = JsonSerializer.Serialize(character.Emotions),
                        desires = JsonSerializer.Serialize(character.Desires)
                    });
                });
            }
            finally
            {
                await session.CloseAsync();
            }
        }

        public async Task<Character?> GetCharacterByIdAsync(string id)
        {
            var session = _driver.AsyncSession();
            try
            {
                return await session.ExecuteReadAsync(async tx =>
                {
                    var query = "MATCH (c:Character {id: $id}) RETURN c";
                    var result = await tx.RunAsync(query, new { id });
                    var record = await result.SingleAsync();

                    if (record == null) return null;

                    var node = record["c"].As<INode>();
                    return new Character
                    {
                        Id = node["id"].As<string>(),
                        Name = node["name"].As<string>(),
                        LlmProvider = node["llm_provider"].As<string>(),
                        Personality = node["personality"].As<string>(),
                        Background = node["background"].As<string>(),
                        Values = JsonSerializer.Deserialize<Dictionary<string, float>>(node["values"].As<string>()) ?? new(),
                        Emotions = JsonSerializer.Deserialize<Dictionary<string, float>>(node["emotions"].As<string>()) ?? new(),
                        Desires = JsonSerializer.Deserialize<Dictionary<string, float>>(node["desires"].As<string>()) ?? new()
                    };
                });
            }
            catch (InvalidOperationException) // SingleAsync throws if no element
            {
                return null;
            }
            finally
            {
                await session.CloseAsync();
            }
        }
    }
}
