# Android App Development Guide

This guide will help you create an Android app to interact with your LLM ChatBot backend.

## Project Structure

```
android/
├── app/
│   ├── src/main/
│   │   ├── java/com/llmchatbot/
│   │   │   ├── MainActivity.java
│   │   │   ├── ChatActivity.java
│   │   │   ├── ApiService.java
│   │   │   └── models/
│   │   │       ├── ChatMessage.java
│   │   │       ├── ChatRequest.java
│   │   │       └── ChatResponse.java
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   ├── activity_main.xml
│   │   │   │   └── activity_chat.xml
│   │   │   ├── values/
│   │   │   │   └── strings.xml
│   │   │   └── drawable/
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
└── settings.gradle
```

## Dependencies

Add these dependencies to your `app/build.gradle`:

```gradle
dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.recyclerview:recyclerview:1.3.0'
    
    // Networking
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.11.0'
    
    // JSON handling
    implementation 'com.google.code.gson:gson:2.10.1'
    
    // Async operations
    implementation 'androidx.lifecycle:lifecycle-viewmodel:2.7.0'
    implementation 'androidx.lifecycle:lifecycle-livedata:2.7.0'
}
```

## API Service

Create `ApiService.java`:

```java
package com.llmchatbot;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Url;

public interface ApiService {
    @POST("api/chat")
    Call<ChatResponse> sendMessage(@Body ChatRequest request);
    
    @GET("api/health")
    Call<HealthResponse> checkHealth();
    
    @POST("api/conversation/clear")
    Call<Void> clearConversation();
}
```

## Data Models

Create `ChatMessage.java`:

```java
package com.llmchatbot.models;

public class ChatMessage {
    private String role;
    private String content;
    private String timestamp;
    
    // Constructors, getters, setters
    public ChatMessage() {}
    
    public ChatMessage(String role, String content) {
        this.role = role;
        this.content = content;
    }
    
    // Getters and setters
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
    
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    
    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
}
```

Create `ChatRequest.java`:

```java
package com.llmchatbot.models;

import java.util.List;

public class ChatRequest {
    private String message;
    private List<ChatMessage> conversation_history;
    
    public ChatRequest(String message, List<ChatMessage> history) {
        this.message = message;
        this.conversation_history = history;
    }
    
    // Getters and setters
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    
    public List<ChatMessage> getConversation_history() { return conversation_history; }
    public void setConversation_history(List<ChatMessage> conversation_history) { 
        this.conversation_history = conversation_history; 
    }
}
```

Create `ChatResponse.java`:

```java
package com.llmchatbot.models;

import java.util.List;

public class ChatResponse {
    private String response;
    private List<ChatMessage> conversation_history;
    private String model_used;
    private double processing_time;
    
    // Getters and setters
    public String getResponse() { return response; }
    public void setResponse(String response) { this.response = response; }
    
    public List<ChatMessage> getConversation_history() { return conversation_history; }
    public void setConversation_history(List<ChatMessage> conversation_history) { 
        this.conversation_history = conversation_history; 
    }
    
    public String getModel_used() { return model_used; }
    public void setModel_used(String model_used) { this.model_used = model_used; }
    
    public double getProcessing_time() { return processing_time; }
    public void setProcessing_time(double processing_time) { this.processing_time = processing_time; }
}
```

## Main Activity

Create `MainActivity.java`:

```java
package com.llmchatbot;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        Button startChatButton = findViewById(R.id.start_chat_button);
        startChatButton.setOnClickListener(v -> {
            Intent intent = new Intent(this, ChatActivity.class);
            startActivity(intent);
        });
    }
}
```

## Chat Activity

Create `ChatActivity.java`:

```java
package com.llmchatbot;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.llmchatbot.models.*;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import java.util.ArrayList;
import java.util.List;

public class ChatActivity extends AppCompatActivity {
    private RecyclerView recyclerView;
    private ChatAdapter adapter;
    private EditText messageInput;
    private Button sendButton;
    private ApiService apiService;
    private List<ChatMessage> conversationHistory;
    
    private static final String BASE_URL = "http://YOUR_PC_IP:8000/";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);
        
        // Initialize Retrofit
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        apiService = retrofit.create(ApiService.class);
        
        // Initialize UI
        recyclerView = findViewById(R.id.recycler_view);
        messageInput = findViewById(R.id.message_input);
        sendButton = findViewById(R.id.send_button);
        
        conversationHistory = new ArrayList<>();
        
        // Setup RecyclerView
        adapter = new ChatAdapter(conversationHistory);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(adapter);
        
        // Send button click
        sendButton.setOnClickListener(v -> sendMessage());
        
        // Add welcome message
        conversationHistory.add(new ChatMessage("assistant", "Hello! I'm your AI assistant. How can I help you?"));
        adapter.notifyDataSetChanged();
    }
    
    private void sendMessage() {
        String message = messageInput.getText().toString().trim();
        if (message.isEmpty()) return;
        
        // Add user message to UI
        conversationHistory.add(new ChatMessage("user", message));
        adapter.notifyItemInserted(conversationHistory.size() - 1);
        recyclerView.scrollToPosition(conversationHistory.size() - 1);
        
        messageInput.setText("");
        
        // Send to API
        ChatRequest request = new ChatRequest(message, conversationHistory);
        Call<ChatResponse> call = apiService.sendMessage(request);
        
        call.enqueue(new Callback<ChatResponse>() {
            @Override
            public void onResponse(Call<ChatResponse> call, Response<ChatResponse> response) {
                if (response.isSuccessful()) {
                    ChatResponse chatResponse = response.body();
                    conversationHistory.add(new ChatMessage("assistant", chatResponse.getResponse()));
                    adapter.notifyItemInserted(conversationHistory.size() - 1);
                    recyclerView.scrollToPosition(conversationHistory.size() - 1);
                } else {
                    Toast.makeText(ChatActivity.this, "Error: " + response.code(), Toast.LENGTH_SHORT).show();
                }
            }
            
            @Override
            public void onFailure(Call<ChatResponse> call, Throwable t) {
                Toast.makeText(ChatActivity.this, "Network error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
```

## Layout Files

Create `activity_main.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="16dp">
    
    <ImageView
        android:layout_width="120dp"
        android:layout_height="120dp"
        android:src="@drawable/ic_robot"
        android:layout_marginBottom="24dp" />
    
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="LLM ChatBot"
        android:textSize="24sp"
        android:textStyle="bold"
        android:layout_marginBottom="8dp" />
    
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="AI-powered chatbot with local LLM"
        android:textSize="16sp"
        android:textColor="#666"
        android:layout_marginBottom="32dp" />
    
    <Button
        android:id="@+id/start_chat_button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Start Chat"
        android:textSize="18sp"
        android:padding="16dp" />
    
</LinearLayout>
```

Create `activity_chat.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
    
    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/recycler_view"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:padding="8dp" />
    
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="8dp">
        
        <EditText
            android:id="@+id/message_input"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:hint="Type your message..."
            android:padding="12dp" />
        
        <Button
            android:id="@+id/send_button"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Send"
            android:layout_marginStart="8dp" />
        
    </LinearLayout>
    
</LinearLayout>
```

## Network Configuration

Add to `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

<application
    android:usesCleartextTraffic="true"
    ... >
```

## Important Notes

1. **Replace YOUR_PC_IP**: Update the BASE_URL with your PC's IP address
2. **Network Security**: The app uses cleartext traffic for local development
3. **Error Handling**: Add proper error handling and loading states
4. **UI Polish**: Customize the chat adapter for better message display
5. **Testing**: Test on the same network as your PC

## Next Steps

1. Create the Android project in Android Studio
2. Add the dependencies
3. Implement the code files
4. Test the connection to your backend
5. Customize the UI and add features
