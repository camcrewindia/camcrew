import React from 'react';
import { View, Text, StyleSheet, ScrollView, Alert } from 'react-native';
import { useTheme } from '../../hooks/useTheme';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { EarningsChart } from '../../components/charts/EarningsChart';
import { Badge } from '../../components/ui/Badge';
import { DollarSign, Download, ArrowUpRight } from 'lucide-react-native';

export const EarningsScreen: React.FC = () => {
  const { colors } = useTheme();

  return (
    <ScrollView style={[styles.container, { backgroundColor: colors.background }]} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: colors.textPrimary }]}>Earnings & Payouts</Text>
      </View>

      <Card style={styles.heroCard}>
        <Text style={[styles.heroLabel, { color: colors.textFaint }]}>Lifetime Net Earnings</Text>
        <Text style={[styles.heroValue, { color: colors.accent }]}>₹3,80,000</Text>
        <Button
          title="Request Instant Payout"
          variant="primary"
          size="md"
          icon={<ArrowUpRight size={16} color="#000000" />}
          onPress={() => Alert.alert('Payout Initiated', 'Payout request sent to Razorpay Route.')}
          style={{ marginTop: 14 }}
        />
      </Card>

      <Card style={styles.card}>
        <EarningsChart />
      </Card>

      <Card style={styles.card}>
        <Text style={[styles.sectionHeading, { color: colors.textPrimary }]}>Recent Payout History</Text>
        <View style={[styles.payoutRow, { borderBottomColor: colors.border }]}>
          <View>
            <Text style={[styles.payoutId, { color: colors.textPrimary }]}>Booking #BK-4092</Text>
            <Text style={[styles.payoutDate, { color: colors.textFaint }]}>August 1, 2026</Text>
          </View>
          <View style={{ alignItems: 'flex-end' }}>
            <Text style={[styles.payoutAmount, { color: colors.success }]}>+₹25,000</Text>
            <Badge label="Paid out" variant="success" />
          </View>
        </View>
      </Card>

      <Button
        title="Download Annual Tax Form 16A (PDF)"
        variant="outline"
        size="lg"
        icon={<Download size={18} color={colors.accent} />}
        onPress={() => Alert.alert('Downloaded', 'Tax document downloaded.')}
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
    padding: 16,
    paddingTop: 64,
    paddingBottom: 115,
  },
  header: {
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: '800',
  },
  heroCard: {
    padding: 20,
    marginBottom: 16,
    borderWidth: 0,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  heroLabel: {
    fontSize: 12,
    textTransform: 'uppercase',
    fontWeight: '600',
  },
  heroValue: {
    fontSize: 32,
    fontWeight: '900',
    marginTop: 4,
  },
  card: {
    marginBottom: 16,
    borderWidth: 0,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  sectionHeading: {
    fontSize: 15,
    fontWeight: '700',
    marginBottom: 10,
  },
  payoutRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
  },
  payoutId: {
    fontSize: 14,
    fontWeight: '700',
  },
  payoutDate: {
    fontSize: 12,
    marginTop: 2,
  },
  payoutAmount: {
    fontSize: 15,
    fontWeight: '800',
  },
});
