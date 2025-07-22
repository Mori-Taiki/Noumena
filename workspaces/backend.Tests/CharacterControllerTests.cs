
using System.Net;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;
using Moq;
using backend.Repositories;
using backend.Models;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.DependencyInjection;

namespace backend.Tests;

public class CharacterControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public CharacterControllerTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task Post_Character_WithValidData_ReturnsCreatedAndCallsRepository()
    {
        // Arrange
        var mockRepo = new Mock<ICharacterRepository>();
        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                services.AddSingleton(mockRepo.Object);
            });
        }).CreateClient();

        var newCharacter = new
        {
            name = "Aragorn",
            llm_provider = "local",
            personality = "The King of Gondor",
            background = "Raised by elves",
        };
        var content = new StringContent(JsonSerializer.Serialize(newCharacter), Encoding.UTF8, "application/json");

        // Act
        var response = await client.PostAsync("/api/characters", content);

        // Assert
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        mockRepo.Verify(repo => repo.CreateCharacterAsync(It.IsAny<Character>()), Times.Once);
    }

    [Fact]
    public async Task Post_Character_WithInvalidData_ReturnsBadRequest()
    {
        // Arrange
        var mockRepo = new Mock<ICharacterRepository>();
        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                services.AddSingleton(mockRepo.Object);
            });
        }).CreateClient();

        var newCharacter = new // name is missing
        {
            llm_provider = "openai",
            personality = "Wise and caring",
            background = "A wizard of the Istari order",
        };
        var content = new StringContent(JsonSerializer.Serialize(newCharacter), Encoding.UTF8, "application/json");

        // Act
        var response = await client.PostAsync("/api/characters", content);

        // Assert
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        mockRepo.Verify(repo => repo.CreateCharacterAsync(It.IsAny<Character>()), Times.Never);
    }

    [Fact]
    public async Task Get_Character_WithExistingId_ReturnsOk()
    {
        // Arrange
        var characterId = "char-123";
        var mockRepo = new Mock<ICharacterRepository>();
        mockRepo.Setup(repo => repo.GetCharacterByIdAsync(characterId))
            .ReturnsAsync(new Character { Id = characterId, Name = "Gandalf" });

        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                services.AddSingleton(mockRepo.Object);
            });
        }).CreateClient();

        // Act
        var response = await client.GetAsync($"/api/characters/{characterId}");

        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var json = await response.Content.ReadAsStringAsync();
        var character = JsonSerializer.Deserialize<Character>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
        Assert.NotNull(character);
        Assert.Equal(characterId, character.Id);
        Assert.Equal("Gandalf", character.Name);
    }

    [Fact]
    public async Task Get_Character_WithNonExistingId_ReturnsNotFound()
    {
        // Arrange
        var characterId = "char-999";
        var mockRepo = new Mock<ICharacterRepository>();
        mockRepo.Setup(repo => repo.GetCharacterByIdAsync(characterId))
            .ReturnsAsync((Character?)null);

        var client = _factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                services.AddSingleton(mockRepo.Object);
            });
        }).CreateClient();

        // Act
        var response = await client.GetAsync($"/api/characters/{characterId}");

        // Assert
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
}
