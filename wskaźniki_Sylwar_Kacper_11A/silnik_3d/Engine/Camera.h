#pragma once
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

class Camera {
private:
    glm::vec3 position;
    glm::vec3 front;
    glm::vec3 up;
    glm::vec3 right;
    glm::vec3 worldUp;

    float yaw;
    float pitch;
    float speed;
    float sensitivity;
    float zoom;

    void updateCameraVectors();

public:
    Camera(glm::vec3 position = glm::vec3(0.0f, 0.0f, 3.0f));

    glm::mat4 getViewMatrix() const;
    glm::mat4 getProjectionMatrix(float aspectRatio) const;

    void processKeyboard(int direction, float deltaTime);
    void processMouseMovement(float xOffset, float yOffset);
    void processMouseScroll(float yOffset);

    glm::vec3 getPosition() const { return position; }
    float getZoom() const { return zoom; }
};