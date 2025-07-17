
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace backend.Models
{
    public class Character
    {
        [JsonPropertyName("id")]
        public string Id { get; set; } = Guid.NewGuid().ToString();

        [Required]
        [JsonPropertyName("name")]
        public string? Name { get; set; }

        [Required]
        [JsonPropertyName("llm_provider")]
        public string? LlmProvider { get; set; }

        [JsonPropertyName("personality")]
        public string? Personality { get; set; }

        [JsonPropertyName("background")]
        public string? Background { get; set; }

        [JsonPropertyName("values")]
        public Dictionary<string, float> Values { get; set; } = new();

        [JsonPropertyName("emotions")]
        public Dictionary<string, float> Emotions { get; set; } = new();

        [JsonPropertyName("desires")]
        public Dictionary<string, float> Desires { get; set; } = new();
    }
}
