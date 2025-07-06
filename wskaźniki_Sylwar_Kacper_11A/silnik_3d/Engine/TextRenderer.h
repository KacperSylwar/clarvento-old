#pragma once

#include <string>
#include <map>
#include <glm/glm.hpp>
#include "Shader.h"

class TextRenderer {
private:
    unsigned int VAO, VBO;
    unsigned int textureID;
    Shader shader;
    std::map<char, struct Character> characters;

    struct Character {
        unsigned int textureID;
        glm::ivec2 size;
        glm::ivec2 bearing;
        unsigned int advance;
    };

public:
    TextRenderer();
    ~TextRenderer();

    bool init();
    void renderText(const std::string& text, float x, float y, float scale, glm::vec3 color);
};