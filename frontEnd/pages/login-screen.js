import { StatusBar } from 'expo-status-bar';
import { useState } from 'react';
import { LinearGradient } from 'expo-linear-gradient';
import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, TextInput} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

function LoginScreen({ navigation }) {

  const login = function(email, password) {
    fetch('http://137.184.103.104:8000/auth/account/login', {
      body: `email_address=${email}&password=${password}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      method: "POST"
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if(data.token !== ""){
        window.localStorage.setItem('token', data.token.toString());
        navigation.navigate('Home')
      }
      else{
        console.log("login failure")
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  return (
    <View style={styles.bg}>
      <LinearGradient colors={['#FFAFBD', '#ffc3a0']} style={styles.gradient}>

      <View style={styles.bg}>
        <TextInput
          style={styles.input}
          placeholder="Email"
          onChangeText={email => setEmail(email)}
          defaultValue={email}
        />

        <TextInput
            secureTextEntry={true}
            style={styles.input}
            placeholder="Password"
            onChangeText={password => setPassword(password)}
            defaultValue={password}
          />

        <TouchableOpacity
          onPress={() => login(email, password)}
          style={styles.button}>
          <Text style={styles.button}>Login</Text>
        </TouchableOpacity>
      </View>
      </LinearGradient>
    </View>
  );
}


const styles = StyleSheet.create({
  bg: {
    flex: 1,
    flexDirection: "column",
  },

  body: {
    flex: 1,
    alignItems: 'center'
  },

  button: {
    color: 'white',
    backgroundColor: '#EC6F66',
    textAlign: 'center',
    fontWeight: 'bold',
    paddingTop: 3,
    margin: 'auto',
    marginBottom: 10,
    fontSize: 15,
    width: '30%',
    borderRadius: 8,
  },

  input: {
    height: 40,
    backgroundColor: '#fff5ef',
    margin: 10,
    borderRadius: 5,
    borderWidth: 2,
    borderColor: '#ffa07a',
    padding: 10
  },
  gradient: {
    flex: 1,
  }
});

export default LoginScreen;
