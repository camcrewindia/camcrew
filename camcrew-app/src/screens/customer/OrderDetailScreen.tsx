import React from 'react';
import { View, Text, StyleSheet, ScrollView, Image, Alert } from 'react-native';
import { useTheme } from '../../hooks/useTheme';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Package, Download, Truck } from 'lucide-react-native';

export const OrderDetailScreen: React.FC<{ navigation: any; route: any }> = ({ navigation, route }) => {
  const { colors } = useTheme();
  const orderId = route?.params?.id || 'ORD-8921';

  return (
    <ScrollView style={[styles.container, { backgroundColor: colors.background }]} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: colors.textPrimary }]}>Order Details</Text>
        <Text style={[styles.orderId, { color: colors.accent }]}>{orderId}</Text>
      </View>

      <Card style={styles.card}>
        <View style={styles.statusRow}>
          <Package size={24} color={colors.accent} />
          <View style={styles.statusMeta}>
            <Text style={[styles.statusTitle, { color: colors.textPrimary }]}>Status: Shipped</Text>
            <Text style={[styles.statusSub, { color: colors.textFaint }]}>Estimated Delivery: 3-5 Days</Text>
          </View>
          <Badge label="In Transit" variant="info" />
        </View>
      </Card>

      <Card style={styles.card}>
        <Text style={[styles.sectionHeading, { color: colors.textPrimary }]}>Shipping Address</Text>
        <Text style={[styles.addrText, { color: colors.textSecondary }]}>Thaha Hussain</Text>
        <Text style={[styles.addrText, { color: colors.textSecondary }]}>Flat 402, Sunset Towers, Bandra West</Text>
        <Text style={[styles.addrText, { color: colors.textSecondary }]}>Mumbai, Maharashtra - 400050</Text>
      </Card>

      <Button
        title="Download Tax Invoice (PDF)"
        variant="outline"
        size="lg"
        icon={<Download size={18} color={colors.accent} />}
        onPress={() => Alert.alert('Invoice Downloaded', 'Tax invoice PDF generated.')}
        style={{ marginVertical: 10 }}
      />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingTop: 68,
  },
  header: {
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: '800',
  },
  orderId: {
    fontSize: 14,
    fontWeight: '700',
    marginTop: 2,
  },
  card: {
    marginBottom: 14,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusMeta: {
    flex: 1,
    marginLeft: 12,
  },
  statusTitle: {
    fontSize: 15,
    fontWeight: '700',
  },
  statusSub: {
    fontSize: 12,
    marginTop: 2,
  },
  sectionHeading: {
    fontSize: 15,
    fontWeight: '700',
    marginBottom: 8,
  },
  addrText: {
    fontSize: 13,
    marginVertical: 2,
  },
});
